import glob
import urlparse
from PIL import Image, ImageDraw
import cStringIO
import base64

from bvgs.serialization.json import load_data_from_json_file

if __name__ == '__main__':
    file_paths = glob.glob('/home/brandverity/opencv_demo/static/images/*.json')
    print 'importing data from contmon'
    for data_file in file_paths:
        print 'reading from', data_file
        page_result = load_data_from_json_file(data_file)
        parsed_url = urlparse.urlparse(page_result['url'])
        domain = parsed_url.netloc
        path = parsed_url.path

        print page_result.keys()
        crawled_pages = list()
        # saving full crawled pages
        print 'url', page_result['url']
        # crawl_url = CrawlUrl.objects.get(url=page_result['url'], path=path, domain=domain)
        for i, screenshot_str in enumerate(page_result['screenshots']):
            page_num = i + 1
            img = Image.open(cStringIO.StringIO(base64.b64decode(screenshot_str)))

            doc = {'id': page_result['url'] + ' ' + str(page_num), 'url': page_result['url'], 'domain': domain,
                   'path': path, 'page_num': page_num,
                   'img_base_64': screenshot_str,
                   'crawled_on': page_result['crawled_on']}

            crawled_pages.append({'path': path, 'image': img, 'domain':domain})


        for j, row in enumerate(page_result['results']):
            crawled_page = crawled_pages[row['page_num'] - 1]
            # html_tree = fromstring(row['html'])
            # #scraper_config = WebsiteScraperConfig.objects.get(domain=domain)
            # row['extracted_fields'] = dict()
            # if scraper_config.selector_style == WebsiteScraperConfig.SELECTOR_STYLE_CSS:
            #     e = html_tree.cssselect(scraper_config.name_selector)
            #     name_element = e[0] if len(e) > 0 else None
            # else:
            #     e = html_tree.find(scraper_config.name_selector)
            #     name_element = e[0] if len(e) > 0  else None
            # if name_element:
            #     row['extracted_fields']['name'] = name_element.text_content().strip()
            # print 'name', row['extracted_fields']['name']
            # row['url_and_page_num'] = {'url': page_result['url'], 'page_num': row['page_num']}
            # row['domain'] = domain
            # row['path'] = path
            # a = path.split('/')[-1].split('-')
            # category = ' '.join(a[:-1])
            # row['category'] = category
            location = row['location']
            size = row['size']
            # TODO: create a method that wraps this on the manager
            # TODO: check if offer with the same hash exist.
            # if it does, offer can happen on many different urls.
            # a url has many offers
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            print 'drawing', location, size
            img = crawled_page['image']
            draw = ImageDraw.Draw(img)
            draw.rectangle([left, top, right, bottom], outline="yellow")
            # new_image = img.crop((left, top, right, bottom))  # defines crop points
        for j, row in enumerate(crawled_pages):
            print 'saving', row['path']+".jpg"
            row['image'].save(row['domain']+"_" + str(j)+".jpg", "jpeg")
