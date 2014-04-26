import args, sys, tempfile, os


from md5digest import Md5Digest

"""
CACHE MANIFEST
CACHE:
NETWORK:
FALLBACK:
#contentmd5=43533453
#md5=2345505
"""
"""
alg:
create new temp manifest
calc checksum of new manifest except for last line
compare checksums
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

    if failover_list:
        opened_file.write("\nFALLBACK:\n")


def write_name_value_comment(opened_file, name, value):
    """adds \nname=value" to the file"""
    opened_file.write("\n#%s=%s"%(name, value))

 


def digest_for_cache_manifest(file_name):
    "return md5 digest for cache file ignoring certain lines"
    try:
        with open(file_name, "r") as cmf:
            md5 = Md5Digest()
            for line in cmf.readlines():
                if not line.startswith("md5="):  ## todo - I think this can go away, no reason to skip md5 since its not there
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







def main():

    # get command line parameters and lists of file specs
    arg_values = args.parse_args(sys.argv[1:])
    cache_arg_files = args.glob_list_of_arg_values(arg_values.cache)
    no_cache_arg_files = args.glob_list_of_arg_values(arg_values.nocache)
    output_manifest_file_name = arg_values.output

    # filter out files in cached list told to not cache
    filenames_to_cache = [ fn for fn in cache_arg_files if fn not in no_cache_arg_files]

    
    # get a temporary file 
    (fd, temp_file_name) = tempfile.mkstemp(prefix="temp_html5appcachegen_")
    os.close(fd)

    # digest value of contents of all cached files
    content_md5_digest = digest_for_content(filenames_to_cache)

    # write temp manifest that reflects the current state
    write_cache_manifest(open(temp_file_name, "w"), filenames_to_cache, arg_values.network, arg_values.fallback)
    write_name_value_comment(open(temp_file_name, "a"), "contentmd5", content_md5_digest)


    #compare the newly created with the old and copy if it has changed
    digest_of_new_manifest = digest_for_cache_manifest(temp_file_name)
    digest_of_old_manifest = digest_for_cache_manifest(output_manifest_file_name)
    if digest_of_old_manifest != digest_of_new_manifest:
        print "digests differ, copying %s to %s"%(temp_file_name, output_manifest_file_name)
        open(output_manifest_file_name, "w").write(open(temp_file_name, "r").read())
    else:
        print "cache manifest contents have not changed"
    

   

    if os.path.exists(temp_file_name):
        os.unlink(temp_file_name)


