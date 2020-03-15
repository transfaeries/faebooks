from pathlib import Path
import os
import pdb

class Faebooks(object):

    def verify_archive(self, archive_filename):
       path_to_archive=Path(archive_filename)
       if not path_to_archive.is_file():
           raise FileNotFoundError(archive_filename + " not found")
        
    
       elif not os.path.getsize(path_to_archive)>0:
           class EmptyFileException(Exception):
               pass
           raise EmptyFileException("Archive File is Empty Please Provide Valid Archive in CSV format")


    def parse_archive(self, archive_filename):
        proper_header=(
            "\"tweet_id\",\"in_reply_to_status_id\","
            "\"in_reply_to_user_id\",\"timestamp\",\"source\","
            "\"text\",\"retweeted_status_id\",\"retweeted_status_user_id\","
            "\"retweeted_status_timestamp\",\"expanded_urls\""
            )
        
        

        pdb.set_trace()
        pass

