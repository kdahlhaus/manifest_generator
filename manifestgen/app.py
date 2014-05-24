import args, sys, tempfile, os, datetime


from md5digest import Md5Digest

"""
CACHE MANIFEST
CACHE:
NETWORK:
FALLBACK:
#contentmd5=43533453
"""

"""
alg:
create new temp manifest
compare digests of new and old manifests
if diff copy new file over to old
"""


def write_cache_manifest(opened_file, cache_list=None, network_list=None, failover_list=None):
    opened_file.write("CACHE MANIFEST\n")

    if cache_list:
        opened_file.write("\nCACHE:\n")
        for fn in cache_list:
            opened_file.write(fn+"\n")

    if network_list:
        opened_file.write("\nNETWORK:\n")
        for n in network_list:
            opened_file.write("%s\n"%(n[0]))

    if failover_list:
        opened_file.write("\nFALLBACK:\n")
        for fb in failover_list:
            opened_file.write("%s %s\n"%(fb[0], fb[1]))


def write_name_value_comment(opened_file, name, value):
    """adds \nname=value" to the file"""
    opened_file.write("\n#%s=%s"%(name, value))

 


def digest_for_cache_manifest(file_name):
    "return md5 digest for cache file ignoring certain lines"
    try:
        with open(file_name, "r") as cmf:
            md5 = Md5Digest()
            for line in cmf.readlines():
                md5.addData(line)
        return md5.digest
    except:
        return -1

def digest_for_content(file_names):
    "return md5 digest for the total contents of files in the list"
    md5 = Md5Digest()
    for file_name in file_names:
        md5.addFile(file_name)
    return md5.digest


def convert_filenames_to_urls( file_names, doc_root=None, url_prefix=None):
    """return list of urls generated by prefixing file_names with url_prefix and considering doc_root on disk as the root of the url tree:
        convert_filenames_to_urls( [ '/usr/proj/index.html', '/usr/proj/js/util.js'], '/usr/proj', '/sample/static' ) = [ '/sample/static/index.html', '/sample/static/js/util.js' ]
    """
    urls = []
    abs_doc_root = os.path.abspath(doc_root) if doc_root else None
    for file_name in file_names:
        # compare file_names with doc_root, truncate everything equal to docroot
        abs_file_name = os.path.abspath(file_name)
        if abs_doc_root and abs_file_name.startswith(abs_doc_root):
            tfn = abs_file_name[len(abs_doc_root):]
        else:
            #remove C: if it's there.  Yes, this is a hack.  Works for me.
            if abs_file_name[1]==":":
                tfn=abs_file_name[2:]
            else:
                tfn = abs_file_name

        # if url_prefix add it
        if url_prefix:
            url = url_prefix + "/" 
        else:
            url = "/"

        url += tfn

        #fix up url
        url = url.replace("\\", "/").replace("//", "/")

        # append to urls
        urls.append(url)        
    
    return urls


def main():

    # get command line parameters and lists of file specs
    arg_values = args.parse_args(sys.argv[1:])
    cache_arg_files = args.glob_list_of_arg_values(arg_values.cache)
    no_cache_arg_files = args.glob_list_of_arg_values(arg_values.nocache)
    output_manifest_file_name = arg_values.output
    doc_root = None if not arg_values.doc_root else arg_values.doc_root[0]
    url_prefix = None if not arg_values.url_prefix else arg_values.url_prefix[0]
    force = arg_values.force

    # filter out files in cached list told to not cache
    filenames_to_cache = [ fn for fn in cache_arg_files if fn not in no_cache_arg_files]

    # get a temporary file 
    (fd, temp_file_name) = tempfile.mkstemp(prefix="temp_manifestgen_")
    os.close(fd)

    #convert file names on disk to urls
    cached_urls = convert_filenames_to_urls(filenames_to_cache, doc_root, url_prefix)

    # digest value of contents of all cached files
    content_md5_digest = digest_for_content(filenames_to_cache)

    # write temp manifest that reflects the current state
    write_cache_manifest(open(temp_file_name, "w"), cached_urls, arg_values.network, arg_values.fallback)
    write_name_value_comment(open(temp_file_name, "a"), "contentmd5", content_md5_digest)

    if force:
        write_name_value_comment(open(temp_file_name, "a"), "timestamp", str(datetime.datetime.now()))

    open(temp_file_name, "a").write("\n") # terminate last line


    #compare the newly created with the old and copy if it has changed
    digest_of_new_manifest = digest_for_cache_manifest(temp_file_name)
    digest_of_old_manifest = digest_for_cache_manifest(output_manifest_file_name)
    if digest_of_old_manifest != digest_of_new_manifest:
        print "digests differ, copying %s to %s"%(temp_file_name, output_manifest_file_name)
        open(output_manifest_file_name, "w").write(open(temp_file_name, "r").read())
    else:
        print "cache manifest contents have not changed"
    

    # remove the temporary file
    if os.path.exists(temp_file_name):
        os.unlink(temp_file_name)
