"""
Custom tags to use in templates or code to render file lists etc. 
    
 History 
 03/09/2012    -     Sjoerd    -    Created this file

"""
import pdb
import datetime
import ntpath
import re
from exceptions import Exception
from os import path
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group,User,Permission
from django.template import RequestContext
from django.utils.html import escape
from profiles.forms import SignupFormExtra
from dataproviders import FileSystemDataProvider
from comicmodels.models import FileSystemDataset, UploadModel, DropboxFolder #FIXME: abstract Dataset should be imported here, not explicit filesystemdataset. the template tag should not care about the type of dataset.
from comicmodels.models import ComicSite, Page
import comicsite.views
from dropbox.rest import ErrorResponse
from dataproviders import FileSystemDataProvider
from dataproviders.DropboxDataProvider import DropboxDataProvider,HtmlLinkReplacer  #TODO: move HtmlLinkReplacer to better location..



def parseKeyValueToken(token):
    """
    Parses the given token string and returns a parameter dictionary
    \param token A string given by the templatetag which is assumes to look like this:
            visualization key1:value1,key2:value2,...
    \return A dictionary
    """
    split = token.split_contents()
    tag = split[0]
    args = split[1:]
    return dict([param.split(":") for param in args])

# This is needed to use the @register.tag decorator
register = template.Library()

@register.simple_tag
def metafooterpages():
    """ Get the metafooter pages. """
    html_string = "<div class='text'><a href=\"/\">COMIC:</a></div>"
    pages = comicsite.views.getPages('COMIC')
    for p in pages:
        if not p.hidden:
            url = reverse('comicsite.views.comicmain', kwargs = {'page_title':p.title})
            html_string += "<a class='metaFooterMenuItem' href='%s'>" % url
            html_string += p.display_title == "" and p.title or p.display_title
            html_string += "</a>"
    return html_string

@register.tag(name = "filelist")
def do_get_files(parser, token):

    try:
        # split_contents() knows not to split quoted strings.
        tag_name, filefolder = token.split_contents()
        format_string = "\"%Y-%m-%d %I:%M %p\""
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return FileListNode(format_string[1:-1], filefolder[1:-1])


class FileListNode(template.Node):
    """ Show list of files in given dir 
    """

    def __init__(self, format_string, filefolder):
        self.format_string = format_string
        self.filefolder = filefolder


    def render(self, context):
        dp = FileSystemDataProvider.FileSystemDataProvider(self.filefolder)

        images = dp.getImages()
        htmlOut = "available files:" + ", ".join(images)
        return htmlOut

@register.tag(name = "dataset")
def render_dataset(parser, token):
    """ Given a challenge and a dataset name, show all files in this dataset as list"""


    usagestr = "Tag usage: {% dataset <datasetname>,<comicsitename> %}. <comicsitename> can be\
                 omitted, defaults to current site"

    #check some basic stuff
    try:
        tag_name, args = token.split_contents()
    except ValueError:
        errormsg = "Error rendering {% " + token.contents + " %}: tag requires at least one \
                    argument. " + usagestr
        #raise template.TemplateSyntaxError(errormsg)        
        return TemplateErrorNode(errormsg)

    if args.count(",") == 0:
        dataset_title = args
        project_name = ""
    elif args.count(",") == 1 :
        dataset_title, project_name = args.split(",")
    else:
        errormsg = "Error rendering {% " + token.contents + " %}: found " + str(args.count(",")) + \
                    " comma's, expected at most 1." + usagestr
        return TemplateErrorNode(errormsg)


    return DatasetNode(dataset_title, project_name)


class DatasetNode(template.Node):
    """ Show list of linked files for given dataset 
    """

    def __init__(self, dataset_title, project_name):
        self.dataset_title = dataset_title
        self.project_name = project_name


    def make_dataset_error_msg(self, msg):
        errormsg = "Error rendering DataSet '" + self.dataset_title + "' for project '" + self.project_name + "': " + msg
        return makeErrorMsgHtml(errormsg)

    def render(self, context):

        if self.project_name == "":
            self.project_name = context.page.comicsite.short_name

        try:        
            dataset = FileSystemDataset.objects.get(comicsite__short_name = self.project_name, title = self.dataset_title)

        except ObjectDoesNotExist as e:
           return self.make_dataset_error_msg("could not find object in database")

        else:
            self.filefolder = dataset.get_full_folder_path()


        dp = FileSystemDataProvider.FileSystemDataProvider(self.filefolder)

        try:
              filenames = dp.getAllFileNames()
        except (OSError) as e:

          return self.make_dataset_error_msg(str(e))


        links = []
        for filename in filenames:

            downloadlink = reverse('filetransfers.views.download_handler_dataset_file', kwargs = {'project_name':dataset.comicsite.short_name,
                                                                                            'dataset_title':dataset.title,
                                                                                            'filename':filename})
            #<a href="{% url filetransfers.views.download_handler_dataset_file project_name='VESSEL12' dataset_title='vessel12' filename='test.png' %}">test </a>
            links.append("<li><a href=\"" + downloadlink + "\">" + filename + " </a></li>")

        description = dataset.description
        htmlOut = description + "<ul class=\"dataset\">" + "".join(links) + "</ul>"

        return htmlOut


@register.tag(name = "visualization")
def render_visualization(parser, token):
    """ Given a dataset name, show a 2D visualization for that """

    usagestr = """Tag usage: {% visualization dataset:string
                                              width:number
                                              height:number
                                              deferredLoad:0|1
                                              extensionFilter:ext1,ext2,ext3
                                              showBrowser:0|1 %}
                  The only mandatory argument is dataset.
                  width/heigth: Size of the 2D view area.
                  defferedLoad: If active, user has to click on the area to load the viewer.
                  extensionFilter: An include filter to specify the file types which should be displayd in the filebrowser.
                  showBrowser: If 1, a file browser is rendered"""
    try:
        args = parseKeyValueToken(token)
    except ValueError:
        errormsg = "Error rendering {% " + token.contents + " %}: Error parsing token. " + usagestr
        return TemplateErrorNode(errormsg)
    

    if "dataset" not in args.keys():
        errormsg = "Error rendering {% " + token.contents + " %}: dataset argument is missing." + usagestr
        return TemplateErrorNode(errormsg)

    return VisualizationNode(args)

class VisualizationNode(template.Node):
    """ 
    Renders a MeVisLab 2D Viewer.
    """

    def __init__(self, args):
        self.args = args

    def make_dataset_error_msg(self, msg):
        errormsg = "Error rendering Visualization '" + str(self.args) + ":" + msg
        return makeErrorMsgHtml(errormsg)

    def render(self, context):
        htmlOut = """
          <div id="comicViewer%(id)d" style="width:%(w)spx; height:%(h)spx"></div>
          <script type="text/javascript">
            var fmeViewer%(id)d = null;
                
            $(document).ready(function (){
              fmeViewer%(id)d = new ComicViewer2D("comicViewer%(id)d", {'deferredLoad':%(deferredLoad)s, 'extensionFilter':'%(extensionFilter)s', 'showBrowser':%(showBrowser)s});
              fmeViewer%(id)d.init(function() {
                fmeViewer%(id)d.setDataRoot('%(path)s');
              });
            });
          </script>
        """ % ({"id": id(self),
                "path": self.args.get("dataset"),
                "w": self.args.get("width", "300"),
                "h": self.args.get("height", "300"),
                "extensionFilter": self.args.get("extensionFilter", ""),
                "deferredLoad": self.args.get("deferredLoad", "0"),
                "showBrowser": self.args.get("showBrowser", "1")})
        return htmlOut


@register.tag(name = "dropbox")
def render_dropbox(parser, token):
    """ Given a django_dropbox item title, render a file from this dropbox """

    usagestr = """Tag usage: {% dropbox title:string file:filepath %}
                  title: the title of an autorized django_dropbox item
                  file: path to a file in your dropbox /apps/COMIC folder                  
                  """
    try:
        args = parseKeyValueToken(token)
    except ValueError:
        errormsg = "Error rendering {% " + token.contents + " %}: Error parsing token. " + usagestr
        return TemplateErrorNode(errormsg)

    if "title" not in args.keys():
        errormsg = "Error rendering {% " + token.contents + " %}: title argument is missing." + usagestr
        return TemplateErrorNode(errormsg)
    
    if "file" not in args.keys():
        errormsg = "Error rendering {% " + token.contents + " %}: file argument is missing." + usagestr
        return TemplateErrorNode(errormsg)

    try:        
        df = DropboxFolder.objects.get(title = args['title'])
    except ObjectDoesNotExist as e:
        return TemplateErrorNode("could not find dropbox titled '"+args['title']+"' in database")
        
    provider = df.get_dropbox_data_provider()
    replacer = HtmlLinkReplacer()

    return DropboxNode(args,df,provider,replacer)


class DropboxNode(template.Node):
    def __init__(self, args, df, provider,replacer):
        self.args = args
        self.df = df
        self.provider = provider
        self.replacer = replacer

    def make_dropbox_error_msg(self, msg):
        errormsg = "Error rendering dropbox '" + str(self.args) + ": " + msg
        return makeErrorMsgHtml(errormsg)

    def render(self, context):

        try:            
            contents = self.provider.read(self.args["file"])
        except ErrorResponse as e:
            return self.make_dropbox_error_msg(str(e))
        
        # any relative link inside included file has to be replaced to make it work within the COMIC
        # context.
        baseURL = reverse('comicsite.views.dropboxpage',kwargs={'site_short_name':context.page.comicsite.short_name,
                                                                'page_title':context.page.title,
                                                                'dropboxname':self.args['title'],
                                                                'dropboxpath':"remove"})
        # for some reason reverse matching does not work for emtpy dropboxpath (maybe views.dropboxpage
        # throws an error?. Workaround is to add 'remove' as path and chop this off the returned link
        # nice.        
        baseURL = baseURL[:-7] #remove "remove/" from baseURL
        currentpath =  ntpath.dirname(self.args['file']) + "/"  # path of currently rendered dropbox file 
                                                
        replaced = self.replacer.replace_links(contents,baseURL,currentpath)          
        htmlOut = replaced
        
        return htmlOut

#{% insertfile results/test.txt %}
@register.tag(name = "insert_file")
def insert_file(parser, token):    
    """ Render a file from the local dropbox folder of the current project"""

    usagestr = """Tag usage: {% insertfile <file> %} 
                  <file>: filepath relative to project dropboxfolder.
                  Example: {% insertfile results/test.txt %}
                  You can use url parameters in <file> by using {{curly braces}}.
                  Example: {% insterfile {{id}}/result.txt %} called with ?id=1234 
                  appended to the url will show the contents of "1234/result.txt".                                                                       
                  """
    
    split = token.split_contents()
    tag = split[0]
    all_args = split[1:]
    
    if len(all_args) != 1:
        error_message = "Expected 1 argument, found " + str(len(all_args))
        return TemplateErrorNode(error_message)
    else:        
        args = {}
        args["file"] = all_args[0]

    replacer = HtmlLinkReplacer()
    
    return InsertFileNode(args,replacer)


class InsertFileNode(template.Node):
    def __init__(self, args,replacer):
        self.args = args
        self.replacer = replacer

    def make_error_msg(self, msg):        
        errormsg = "Error including file '" + "," + self.args["file"] + "': " + msg
        return makeErrorMsgHtml(errormsg)
    
    def substitute(self,string,substitutions):
        """
        Take each key in the substitutions dict. See if this key exists
        between double curly braces in string. If so replace with value.        
        
        Example: 
        substitute("my name is {{name}}.",{version:1,name=John})
        > "my name is John"
        """
        
        for key,value in substitutions:
            string = re.sub("{{"+key+"}}",value,string)
        
        return string
        
        

    def render(self, context):
        
        # allow url parameter file=<filename> to overwrite any filename given as arg
        # TODO: in effect any file can now be included by anyone using a url addition.
        # This feels quite powerful but also messy. Is this proper? Redeeming fact: One can only access files
        # inside DROPBOX_ROOT.. 
        # TODO: does accessing a file "..\..\..\..\allyoursecrets.txt" work?
        # TODO: designate variables more clearly. having any string possibly be a var seems messy
        
        # context["request"].GET contains a queryDict of all url parameters.
        
        filename_raw = self.args['file']                
        filename_clean = self.substitute(filename_raw,context["request"].GET.items())
        
        # If any url parameters are still in filename they were not replaced. This filename
        # is missing information..
        if re.search("{{\w+}}",filename_clean):
            
            missed_parameters = re.findall("{{\w+}}",filename_clean)
            found_parameters = context["request"].GET.items()
                    
            if found_parameters == []:
                found_parameters = "None"
            error_msg = "I am missing required url parameter(s) %s, url parameter(s) found: %s "\
                        "" % (missed_parameters, found_parameters)             
            return self.make_error_msg(error_msg)
                 
        project_name = context.page.comicsite.short_name
        filename = path.join(settings.DROPBOX_ROOT,project_name,filename_clean)                    
        
        try:            
            contents = open(filename,"r").read()
        except Exception as e:
            return self.make_error_msg(str(e))
        
        #TODO check content safety
        
        # any relative link inside included file has to be replaced to make it work within the COMIC
        # context.
        base_url = reverse('comicsite.views.insertedpage',kwargs={'site_short_name':context.page.comicsite.short_name,
                                                                'page_title':context.page.title,
                                                                'dropboxpath':"remove"})
        # for some reason reverse matching does not work for emtpy dropboxpath (maybe views.dropboxpage
        # throws an error?. Workaround is to add 'remove' as path and chop this off the returned link
        # nice.        
        base_url = base_url[:-7] #remove "remove/" from baseURL
        current_path =  ntpath.dirname(filename_clean) + "/"  # path of currently inserted file 
                      
                                  
        replaced = self.replacer.replace_links(contents,base_url,current_path)          
        html_out = replaced
        
        #rewrite relative links
        
        return html_out
    

@register.tag(name = "url_parameter")
def url_parameter(parser, token):    
    """ Try to read given variable from given url. """

    usagestr = """Tag usage: {% url_parameter <param_name> %} 
                  <param_name>: The parameter to read from the requested url.
                  Example: {% url_parameter name %} will write "John" when the
                  requested url included ?name=John.                                    
                  """
    
    split = token.split_contents()
    tag = split[0]
    all_args = split[1:]
    
    if len(all_args) != 1:
        error_message = "Expected 1 argument, found " + str(len(all_args))
        return TemplateErrorNode(error_message)
    else:        
        args = {}
        args["url_parameter"] = all_args[0]
    
    args["token"] = token

    return UrlParameterNode(args)


class UrlParameterNode(template.Node):
    
    def __init__(self, args):
        self.args = args
    
    def make_error_msg(self, msg):
        errormsg = "Error including file '" + ",".join(self.args) + "': " + msg
        return makeErrorMsgHtml(errormsg)

    def render(self, context):  
             
        #request= context["request"].GET[]
        if context['request'].GET.has_key(self.args['url_parameter']): 
            return context['request'].GET[self.args['url_parameter']] # FIXME style: is this too much in one line?
        else:
            error_message = "Error rendering %s: Parameter '%s' not found in request URL" % ("{%  "+self.args['token'].contents +"%}",
                                                                                             self.args['url_parameter'])
            return makeErrorMsgHtml(error_message)
        


@register.tag(name = "all_projects")
def render_all_projects(parser, token):
    """ Render an overview of all projects """

    try:
        projects = ComicSite.objects.non_hidden()
    except ObjectDoesNotExist as e:
        errormsg = "Error rendering {% " + token.contents + " %}: Could not find any comicSite object.."
        return TemplateErrorNode(errormsg)

    return AllProjectsNode(projects)

class AllProjectsNode(template.Node):
    """ return html list listing all projects in COMIC 
    """

    def __init__(self, projects):
        self.projects = projects

    def render(self, context):
        html = ""
        for project in self.projects:
            html += comicsite.views.comic_site_to_html(project)
        return html


@register.tag(name = "image_url")
def render_image_url(parser, token):
    """ render image based on image title """
    # split_contents() knows not to split quoted strings.
    tag_name, args = token.split_contents()
    imagetitle = args

    try:
        image = UploadModel.objects.get(title = imagetitle)

    except ObjectDoesNotExist as e:

        errormsg = "Error rendering {% " + token.contents + " %}: Could not find any images named '" + imagetitle + "' in database."
        #raise template.TemplateSyntaxError(errormsg)
        return TemplateErrorNode(errormsg)

    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    [isImage, errorMessage] = hasImgExtension(str(image.file))
    if not isImage:
        errormsg = "Error rendering {% " + token.contents + " %}:" + errorMessage
        #raise template.TemplateSyntaxError(errormsg)
        return TemplateErrorNode(errormsg)


    return imagePathNode(image)



class imagePathNode(template.Node):
    """ return local path to the given UploadModel 
    """

    def __init__(self, image):
        self.image = image

    def render(self, context):
        path = "/static/media/" + str(self.image.file)

        return path


@register.tag(name = "registration")
def render_registration_form(parser, token):
    """ Render a registration form for the current site """

    try:
        projects = ComicSite.objects.all()
    except ObjectDoesNotExist as e:
        errormsg = "Error rendering {% " + token.contents + " %}: Could not find any comicSite object.."
        return TemplateErrorNode(errormsg)

    return RegistrationFormNode(projects)



class RegistrationFormNode(template.Node):
    """ return HTML form of registration, which links to main registration 
    Currently just links to registration
    """

    def __init__(self, projects):
        self.projects = projects

    def render(self, context):
        sitename = context.page.comicsite.short_name
        pagetitle = context.page.title
        signup_url = reverse('userena_signin') + "?next=" \
                     + reverse('comicsite.views.page', kwargs = {'site_short_name':sitename, 'page_title':pagetitle})
        signuplink = makeHTMLLink(signup_url, "sign in")
        registerlink = makeHTMLLink(reverse('userena.views.signup',
                                             kwargs = {'signup_form':SignupFormExtra}), "register")

        
        if not context['user'].is_authenticated():
            return "To register for " + sitename + ", you need be logged in to COMIC.\
            please " + signuplink + " or " + registerlink

        else:
            participantsgroup = Group.objects.get(name=context.page.comicsite.participants_group_name())
            if participantsgroup in context['user'].groups.all():
                msg = "You have already registered for " + sitename
            else:
                register_url = reverse('comicsite.views._register', kwargs = {'site_short_name':sitename}) 
                msg = makeHTMLLink(register_url, "Register for " + sitename)
            return msg 





class TemplateErrorNode(template.Node):
    """Render error message in place of this template tag. This makes it directly obvious where the error occured
    """
    def __init__(self, errormsg):
        self.msg = HTML_encode_django_chars(errormsg)

    def render(self, context):
        return makeErrorMsgHtml(self.msg)


def HTML_encode_django_chars(string):
    """replace curly braces and percent signs by their html encoded equivolents    
    """ 
    string = string.replace("{","&#123;")
    string = string.replace("}","&#125;")
    string = string.replace("%","&#37;")    
    return string

def makeHTMLLink(url, linktext):
    return "<a href=\"" + url + "\">" + linktext + "</a>"

def hasImgExtension(filename):

    allowedextensions = [".jpg", ".jpeg", ".gif", ".png", ".bmp"]
    ext = path.splitext(filename)[1]
    if ext in allowedextensions:
         return [True, ""]
    else:
         return [False, "file \"" + filename + "\" does not look like an image. Allowed extensions: [" + ",".join(allowedextensions) + "]"]


def makeErrorMsgHtml(text):
     errorMsgHTML = "<p><span class=\"pageError\"> " + HTML_encode_django_chars(text) + " </span></p>"
     return errorMsgHTML;