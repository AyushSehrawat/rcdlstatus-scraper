def get_dl_xpath_consts() -> dict:
    return {
        'captcha_error_summary_xpath': '//span[@class="ui-messages-error-summary"]',
        'captcha_error_detail_xpath': '//span[@class="ui-messages-error-detail"]',
        'dl_error_xpath': '//body/script',
        'dl_current_status_xpath': '//*[@id="form_rcdl:j_idt85"]/table[1]/tr/td[2]/span/text()',
        'dl_holder_name_xpath': '//*[@id="form_rcdl:j_idt85"]/table[1]/tr/td[2]/text()',
        'dl_old_new_dlno_xpath': '//*[@id="form_rcdl:j_idt85"]/table[1]/tr/td[2]/text()',
        'dl_source_of_data_xpath': '//*[@id="form_rcdl:j_idt85"]/table[1]/tr/td[2]/text()',
        'dl_initial_issue_date_xpath': '//*[@id="form_rcdl:j_idt85"]/table[2]/tr/td[2]/text()',
        'dl_initial_issuing_office_xpath': '//*[@id="form_rcdl:j_idt85"]/table[2]/tr/td[2]/text()',
        'dl_last_endorsed_date_xpath': '//*[@id="form_rcdl:j_idt85"]/table[3]/tr/td[2]/text()',
        'dl_last_endorsed_office_xpath': '//*[@id="form_rcdl:j_idt85"]/table[3]/tr/td[2]/text()',
        'dl_last_completed_transaction_xpath': '//*[@id="form_rcdl:j_idt85"]/table[3]/tr/td[2]/text()',
        'dl_nt_from_xpath': '//*[@id="form_rcdl:j_idt85"]/table[4]/tr/td[2]/text()',
        'dl_t_from_xpath': '//*[@id="form_rcdl:j_idt85"]/table[4]/tr/td[2]/text()',
        'dl_nt_to_xpath': '//*[@id="form_rcdl:j_idt85"]/table[4]/tr/td[3]/text()',
        'dl_t_to_xpath': '//*[@id="form_rcdl:j_idt85"]/table[4]/tr/td[3]/text()',
        'dl_hazardous_valid_till_xpath': '//*[@id="form_rcdl:j_idt85"]/table[5]/tr/td[2]/text()',
        'dl_hill_valid_till_xpath': '//*[@id="form_rcdl:j_idt85"]/table[5]/tr/td[4]/text()',
        'dl_cov_categories_xpath': '//*[@id="form_rcdl:j_idt137"]//table//tbody//td[1]/text()',
        'dl_class_of_vehicle_xpath': '//*[@id="form_rcdl:j_idt137"]//table//tbody//td[2]/text()',
        'dl_cov_issue_date_xpath': '//*[@id="form_rcdl:j_idt137"]//table//tbody//td[3]/text()'
    }