import re
import json
import requests
from lxml import html
import cv2
import numpy as np
import pytesseract
from dl_xpath_consts import get_dl_xpath_consts

class ParivahanDL:
    def __init__(self):
        self.session = requests.Session()
        self.parivahan_dl_url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"
        self.parivahan_dl_post = "https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml"
        self.dl_no_form_id = "form_rcdl:tf_dlNO"
        self.dl_dob_form_id = "form_rcdl:tf_dob_input"
        self.dl_captcha_form_id = "form_rcdl:j_idt39:CaptchaID"
        self.view_state_xpath = '//*[@id="j_id1:javax.faces.ViewState:0"]'
        self.captcha_image_xpath= '//*[@id="form_rcdl:j_idt39:j_idt47"]'
        self.dl_xpath_consts = get_dl_xpath_consts()
        self.get_page = None
        self.captcha_image = None
        self.view_state = None
        self.jsessionid = None
        self.headers = None
        self.data = None

    def initialize(self):
        self.get_page = html.fromstring(self.session.get(self.parivahan_dl_url).content)
        self.captcha_image = "https://parivahan.gov.in" + self.get_page.xpath(self.captcha_image_xpath)[0].get(
            "src"
        )
        self.view_state = self.get_page.xpath(self.view_state_xpath)[0].get("value")
        jsessionid_regex = re.search(r';jsessionid=(\w+)', self.captcha_image)
        self.jsessionid = jsessionid_regex.group(1)
        self.headers = {
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": self.parivahan_dl_url,
            "Cookie": f"JSESSIONID={self.jsessionid}; SERVERID_parivahan_73=parivahanapp1; has_js=1; SERVERID_parivahan_81=parivahanapp3_81",
        }
        self.data = {
            # "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form_rcdl:j_idt53",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl",
            "form_rcdl:j_idt53": "form_rcdl:j_idt53",
            "form_rcdl": "form_rcdl",
            "javax.faces.ViewState": self.view_state,   
        }

    @staticmethod
    def replace_chars(text) -> str:
        alphanumeric_text = re.sub(r'\W+', '', text)
        return alphanumeric_text

    def get_captcha(self) -> str:
        try:
            response = requests.get(self.captcha_image)
            img = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
            gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thr = cv2.adaptiveThreshold(gry, 181, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 10)
            txt = pytesseract.image_to_string(thr, lang='eng', config='--psm 10 --oem 3')
            result = self.replace_chars(txt)
            return result
        except Exception as e:
            print(e)
            return ""
        
    def get_dl_details(self, dl_no, dl_dob) -> dict:
        self.data[self.dl_no_form_id] = dl_no
        self.data[self.dl_dob_form_id] = dl_dob

        max_attempts = 50
        attempts = 0

        while True and attempts < max_attempts:
            dl_captcha = self.get_captcha()
            self.data[self.dl_captcha_form_id] = dl_captcha

            post_resp = self.session.post(self.parivahan_dl_post, headers=self.headers, data=self.data)
            post_page = html.fromstring(post_resp.content)

            if post_page.xpath(self.dl_xpath_consts["captcha_error_summary_xpath"]):
                error = {
                    "success": False,
                    "error_summary": post_page.xpath(self.dl_xpath_consts["captcha_error_summary_xpath"])[0].text,
                    "error_detail": post_page.xpath(self.dl_xpath_consts["captcha_error_detail_xpath"])[0].text,
                }
                print(json.dumps(error, indent=4))
                attempts += 1
                print(f"Attempt {attempts}/{max_attempts}")

                if attempts == max_attempts:
                    return {
                        "success": False,
                        "error_summary": "Max attempts reached",
                        "error_detail": "Please try again later",
                    }
                else:
                    continue  # loop until captcha is correct

            elif post_page.xpath(self.dl_xpath_consts["dl_error_xpath"]):
                error = {
                    "success": False,
                    "error_summary": "Invalid DL Number or DOB",
                    "error_detail": "Please check your DL Number and DOB",
                }
                return error  # no need to continue if DL/DOB is invalid
            
            else:
                try:
                    dl_data = {
                        "dl_current_status": post_page.xpath(self.dl_xpath_consts["dl_current_status_xpath"])[0],
                        "dl_holder_name": post_page.xpath(self.dl_xpath_consts["dl_holder_name_xpath"])[0],
                        "dl_old_new_dlno": post_page.xpath(self.dl_xpath_consts["dl_old_new_dlno_xpath"])[1],
                        "dl_source_of_data": post_page.xpath(self.dl_xpath_consts["dl_source_of_data_xpath"])[2],
                        "dl_initial_issue_date": post_page.xpath(self.dl_xpath_consts["dl_initial_issue_date_xpath"])[0],
                        "dl_initial_issuing_office": post_page.xpath(self.dl_xpath_consts["dl_initial_issuing_office_xpath"])[1],
                        "dl_last_endorsed_date": post_page.xpath(self.dl_xpath_consts["dl_last_endorsed_date_xpath"])[0],
                        "dl_last_endorsed_office": post_page.xpath(self.dl_xpath_consts["dl_last_endorsed_office_xpath"])[1],
                        "dl_last_completed_transaction": post_page.xpath(self.dl_xpath_consts["dl_last_completed_transaction_xpath"])[2],
                        "dl_nt_from": post_page.xpath(self.dl_xpath_consts["dl_nt_from_xpath"])[0],
                        "dl_t_from": post_page.xpath(self.dl_xpath_consts["dl_t_from_xpath"])[1],
                        "dl_nt_to": post_page.xpath(self.dl_xpath_consts["dl_nt_to_xpath"])[0],
                        "dl_t_to": post_page.xpath(self.dl_xpath_consts["dl_t_to_xpath"])[1],
                        "dl_hazardous_valid_till": post_page.xpath(self.dl_xpath_consts["dl_hazardous_valid_till_xpath"])[0],
                        "dl_hill_valid_till": post_page.xpath(self.dl_xpath_consts["dl_hill_valid_till_xpath"])[0],
                    }

                    dl_cov_categories = post_page.xpath(self.dl_xpath_consts["dl_cov_categories_xpath"])
                    dl_class_of_vehicle = post_page.xpath(self.dl_xpath_consts["dl_class_of_vehicle_xpath"])
                    dl_cov_issue_date = post_page.xpath(self.dl_xpath_consts["dl_cov_issue_date_xpath"])

                    dl_cov_details = []
                    for dl_cov_category, dl_class_of_vehicle, dl_cov_issue_date in zip(dl_cov_categories, dl_class_of_vehicle, dl_cov_issue_date):
                        dl_cov_details.append({
                            "dl_cov_categories": dl_cov_category,
                            "dl_class_of_vehicle": dl_class_of_vehicle,
                            "dl_cov_issue_date": dl_cov_issue_date
                        })

                    dl_data["dl_cov_details"] = dl_cov_details
                    dl_data["success"] = True
                    return dl_data
                except Exception as e:
                    print(e)
                    return {
                        "success": False,
                        "message": "Error while fetching DL details",
                        "details": "Probably due to incorrect xpath. Xpath required to be updated."
                    }
                

if __name__ == "__main__":
    dl_no = "MH03-20080022135"
    dl_dob = "01-12-1987"

    dl = ParivahanDL()
    dl.initialize()
    dl_data = dl.get_dl_details(dl_no, dl_dob)
    print(json.dumps(dl_data, indent=4))