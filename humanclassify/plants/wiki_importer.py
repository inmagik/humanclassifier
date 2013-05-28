import mwclient
import re
import urllib
from pymongo import MongoClient
box_title = None

exp = r'\{\{'                  # the opening brackets for the infobox 
exp = exp + r'\s*'           # any amount of whitespace
exp = exp + r'([Tt]axobox|[Ii]nfobox)'  # the word "infobox", capitalized or not followed by at least one space
exp = exp + r'.*'           # a bunch of other stuff in the infobox  
exp3 = exp                  # save the regexp so far so that I can use it later
exp3 = exp3 + r'.*\}\}'          # any amount of anything, followed by the end of the infobox

exp3_obj = re.compile(exp3, re.DOTALL)
    

EN_WIKIPEDIA_URL = 'en.wikipedia.org'
    
    
class CategoryParser(object):

    def __init__(self, wiki_url=EN_WIKIPEDIA_URL):
        self.wiki_url = wiki_url
        self.site = mwclient.Site(wiki_url)
        
        
    def get_pages_for_category(self, category, DEBUG=True):
        out = []
        try:
            for x in category:
                if DEBUG:
                    print x.page_title
                out.append(x)
                try:
                    out.extend(self.get_pages_for_category(x))
                except:
                    pass
            return out
        
        except:
            return out
        
    def get_pages(self, start_category):
        category = self.site.Pages[start_category] 
        
        pages = self.get_pages_for_category(category)
        return pages
        
        
    def write_to_file(self):
        pass
    
    
    
class PagesFinder(object):
    def __init__(self, filename):
        self.filename = filename
        
        self.backend =  MongoClient()
        self.db = self.backend[filename]
        
        
    def search_category_pages(self, category):
        worker = CategoryParser()
        print "Searching pages..."
        pages = worker.get_pages(category)
        self.put_pages(pages)
        

    def drop_page(self, page):
        collection = self.db['raw_pages']
        collection.remove(page)

        
    def put_pages(self, pages):
        """
        store retrieved pages to backend for later access
        """
        collection = self.db['raw_pages']
        for page in pages:
            print page.page_title
            print "Writing to mongo.."
            page_obj = {'page_title' : page.page_title }
            collection.update(page_obj, page_obj, upsert=True)
        
        
    def put_result(self, index, result):
        """
        stores a result in the backend
        """
        collection = self.db['results']
        q_obj = {'page_title' : result['page_title'] }
        collection.update(q_obj, result, upsert=True)
        
        
        
    def get_pages(self):
        collection = self.db['raw_pages']
        return collection.find()
        
        
    def parse_stored_pages(self, drop=False):
        """
        access stored pages and processes them
        results are put in plants backend
        """
        worker = PageParser()
        pages = self.get_pages()

        done_pages = {}        

        for page in pages:
            page_title = page['page_title']
            if page_title in done_pages:
                continue
            
            box = worker.get_box(page_title)
            
            if box is not None:
                box['page_title'] = page_title
                box['wiki_url'] = "http://" + EN_WIKIPEDIA_URL + "/wiki/" + urllib.quote(page_title)
                try:
                    self.put_result(page_title, box)
                    print "result found!", page_title
                except:
                    pass
            
            done_pages[page_title] = True
            if(drop):
                self.drop_page(page)
            
    def get_results(self):
        collection = self.db['results']
        return collection.find()
    



class PageParser(object):
    def __init__(self, wiki_url=EN_WIKIPEDIA_URL):
        self.wiki_url = wiki_url
        self.site = mwclient.Site(wiki_url)
        
    def get_page_content(self, title):
        page =  self.site.Pages[title]
        images = page.images()
        images_info = []
        for img in images:
            images_info.append(img._info)
        return (page.edit(), images_info)
        
        
    def get_infobox_as_dict(self, title):
        content, images_info = self.get_page_content(title)
        text_piece = self.get_infobox_from_text(content, title)
        data = {}
        if text_piece:
            data['info'] = self.parse_infobox_text(text_piece)
            data['images_info'] = images_info
            #also put content in... for later processing
            data['content'] = content
            return data

        return None
        
        
    def get_box(self, title):
        infobox = self.get_infobox_as_dict(title)
        return infobox
    
    
    
    def get_infobox_from_text(self, article_text, title):
        search_result = exp3_obj.search(article_text)
        if search_result:
            result_text = search_result.group(0) # returns the entire matching sequence
        else:
            print "No match", title
            return None
        # the regex isn't perfect, so look for the closing brackets of the infobox
        count = 0
        last_ind = None
        for ind, c in enumerate(result_text):
            if c == '}':
                count = count -1
            elif c == '{':
                count = count +1
            if count == 0 and not ind == 0:
                last_ind = ind
                break
        return result_text[0:last_ind+1]    
        
    def parse_infobox_text(self, text):
        text = text.split('|')
        text = text[1:] #everything before the first pipe is the infobox declaration
        new_list = [text[0]]
        for item in text[1:]:
            # make sure we split only on the pipes that represent ends of the infobox entry, not the pipes used in links
            if (']]' in item) and ((not '[[' in item) or item.find(']]') < item.find('[[')):
                new_list[-1] = new_list[-1] +'|' + item
            else:
                new_list.append(item)
        new_list[-1] = new_list[-1][:-2] #trim off the closing brackets
        data_dict = {}
        for item in new_list:
            if '=' in item:
                items = item.split('=', 1)
                data_dict[items[0].strip()] = items[1].strip()
            else:
                continue
        return data_dict
            


if __name__ == '__main__':
    #worker = CategoryParser()
    #worker.run('Category:Trees_of_Europe')
    
    worker = PagesFinder("files")
    #worker.search_category_pages("Category:Trees_by_continent")
    worker.search_category_pages("Category:Trees_of_Europe")
    
    worker.parse_stored_pages(drop=True)

    