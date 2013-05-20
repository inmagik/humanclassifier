import mwclient
import re

SPECIES_WIKI = 'species.wikimedia.org'
box_title = None

exp = r'\{\{'                  # the opening brackets for the infobox 
exp = exp + r'\s*'           # any amount of whitespace
exp = exp + r'VN'  # the word "infobox", capitalized or not followed by at least one space
exp = exp + r'.*'           # a bunch of other stuff in the infobox  
exp3 = exp                  # save the regexp so far so that I can use it later
exp3 = exp3 + r'.*\}\}'          # any amount of anything, followed by the end of the infobox

exp3_obj = re.compile(exp3, re.DOTALL)

class PageParser(object):
    def __init__(self, wiki_url=SPECIES_WIKI):
        self.wiki_url = wiki_url
        self.site = mwclient.Site(wiki_url)
        
    def get_page_content(self, title):
        page =  self.site.Pages[title]
        images = page.images()
        images_info = []
        for img in images:
            images_info.append(img._info)
        return (page.edit(), images_info)
        
        
    def get_infobox_as_dict(self, title, content=False, images=False):
        content, images_info = self.get_page_content(title)
        text_piece = self.get_infobox_from_text(content, title)
        data = {}
        if text_piece:
            data['info'] = self.parse_infobox_text(text_piece)
            if images:
                data['images_info'] = images_info
            #also put content in... for later processing
            if content:
                data['content'] = content
            return data

        return None
        
        
    def get_box(self, title, content=False, images=False):
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
    worker = PageParser()
    content = worker.get_box("Fumaria officinalis")
    print content