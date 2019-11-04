# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
from datetime import date
import os

class file_zip(models.TransientModel):
	_inherit = 'hr.payslip.virt'
	
	pass_crypt = fields.Char()

	@api.multi
	def do_export_zip(self):
	    f = open("/home/odoo/virement.txt", "w+")
	    ##### getting employees  ###################################################################
	    if self.payslip_char:
	        payslip_ids = self.payslip_char.split(",")
	        pay = []
	        for pay_line in payslip_ids:
	            pay.append(int(pay_line))
	        payslips = self.env['hr.payslip'].browse(pay)

	    else:
	        payslips = False
	    #payslips  = self.payslip_ids

	    ###### data company #######################################################################
	    company_name = self.env['res.company'].browse([1]).name
	    if len(company_name) < 25:
	        count_name = 25-len(company_name)
	        for i in range(1,count_name):
	            company_name += ' '
	    else:
	        company_name = company_name[:24]
	    today = date.today()
	    day_month = today.strftime("%d%m")
	    years = today.strftime("%Y")
	    modif_years = years[3]
	    result = (day_month + modif_years)
	    data_company = ['0302',
	                    '        ',
	                    '      ',
	                    '       ',
	                    result,
	                    company_name.upper(),
	                    '       ',
	                    '                         ',
	                    '00004',
	                    '01206420101',
	                    '                ',
	                    '                       ',
	                    '        ',
	                    '00004',
	                    '000000\n']
	    for line_data_company in data_company:
	        f.write(str(line_data_company))

	    ###### montant total dans txt #####################
	    amount_total = 0
	    ###### end montant total ##########################
	    if payslips:
	        m = 0
	        for payslip in payslips:
	            ###### ref employee #####################
	            len_count = 7 - len(str(m))
	            start_char = ""
	            for middle_char in range(1,len_count):
	                start_char += "0"
	            ref_emp = "B" + start_char + str(m)

	            ###### end ref employee #################

	            ####### name of employee ###############
	            nom = payslip.employee_id.nom
	            if len(nom) < 25:
	                count_name = 25-len(nom)
	                for i in range(1,count_name):
	                    nom += ' '
	            else:
	                nom = nom[:24]

	            ####### end name of employee ###########

	            ####### getiing bank ###################
	            nom_banque = ""
	            if payslip.employee_id.bank_account_id.bank_id.name:
	                nom_banque = payslip.employee_id.bank_account_id.bank_id.name
	            if nom_banque:
	                if len(nom_banque) < 8:
	                    count_name = 8-len(nom_banque)
	                    for i in range(1,count_name):
	                        nom_banque += ' '
	                else:
	                    nom_banque = nom_banque[:7]
	            else:
	                nom_banque = '       '
	            ####### end getting bank #################

	            ####### getting code agence ##############
	            code_agence = ""
	            if payslip.employee_id.bank_account_id.acc_number:
	                code_agence = payslip.employee_id.bank_account_id.acc_number
	                code_agence = code_agence[5:10]
	            if code_agence:
	                if len(code_agence) < 6:
	                    count_name = 6-len(code_agence)
	                    for i in range(1,count_name):
	                        code_agence += ' '
	                else:
	                    code_agence = code_agence[5:10]
	            else:
	                code_agence = '     '
	            ####### ending getting compte ############


	            ####### getting num compte ##############
	            num_compte = ""
	            if payslip.employee_id.bank_account_id.acc_number:
	                num_compte = payslip.employee_id.bank_account_id.acc_number
	                num_compte = num_compte[10:21]
	            if num_compte:
	                if len(num_compte) < 12:
	                    count_name = 12-len(num_compte)
	                    for i in range(1,count_name):
	                        num_compte += ' '
	                else:
	                    num_compte = num_compte[10:21]
	            else:
	                num_compte = '           '
	            ####### ending getting compte ############

	            ####### getting code bank ##############
	            code_bank = ""
	            if payslip.employee_id.bank_account_id.acc_number:
	                code_bank = payslip.employee_id.bank_account_id.acc_number
	                code_bank = code_bank[:5]
	            if code_bank:
	                if len(code_bank) < 6:
	                    count_name = 6-len(code_bank)
	                    for i in range(1,count_name):
	                        code_bank += ' '
	                else:
	                    code_bank = code_bank[:5]
	            else:
	                code_bank = '     '
	            ####### ending getting code bank ############

	            ###### montant salaire ##################
	            if payslip.line_ids:
	                for line_id in payslip.line_ids:
	                    if line_id.code == 'NET':
	                        amount = int(line_id.amount)
	                        amount_total += amount
	                        if  len(str(amount)) < 15:
	                            count_name = 15 - len(str(amount))
	                            start_with = ""
	                            for i in range(1,count_name):
	                                start_with += '0'
	                            montant_verse = start_with + str(amount) + "00"

	            else:
	                montant_verse = '0000000000000000'
	            ###### montant salaire ##################
	            ####### reference client ################

	            ####### getting ref client ou intitule bank ##############
	            intitule = ""
	            if self.intitule:
	                intitule = self.intitule
	            if intitule:
	                if len(intitule) < 24:
	                    count_name = 24-len(intitule)
	                    for i in range(1,count_name):
	                        intitule += ' '
	                else:
	                    intitule = intitule[:23]
	            else:
	                intitule = '                       '
	            #ref_client = ref_client[:16]
	            #ref_client = ref_client + '               '
	            ####### reference client ################
	            # ####### code banque ####################
	            # if payslip.employee_id.bank_account_id.bank_id.bic:
	            #     code_bank = payslip.employee_id.bank_account_id.bank_id.bic
	            #     if len(code_bank) < 6:
	            #         num_code_bank = 6 - len(code_bank)
	            #         start_with = ''
	            #         for i in range(1,num_code_bank):
	            #             start_with += '0'
	            #         code_banque = start_with + code_bank
	            #
	            # else:
	            #     code_banque = 00000
	            ####### code banque ####################
	            data_employee = ['0602',
	                            '        ',
	                            '      ',
	                            ref_emp,
	                            '     ',
	                            nom.upper(),
	                            nom_banque,
	                            '                         ',
	                            code_agence,
	                            num_compte,
	                            montant_verse,
	                            intitule,
	                            '        ',
	                            code_bank,
	                            '000000\n']
	            for line_data_employee in data_employee:
	                f.write(str(line_data_employee))
	            m += 1

	    #### ajout derniere ligne ##################
	    montant_verse_total = 0
	    if amount_total == 0:
	        montant_verse_total = '0000000000000000'
	    if  len(str(amount_total)) < 15:
	        count_name = 15 - len(str(amount_total))
	        start_with = ""
	        for i in range(1,count_name):
	            start_with += '0'
	        montant_verse_total = start_with + str(amount_total) + "00"
	    else:
	        montant_verse_total = '0000000000000000'


	    data_company_last = ['0802',
	                    '        ',
	                    '      ',
	                    '       ',
	                    '     ',
	                    '                        ',
	                    '       ',
	                    '                         ',
	                    '                ',
	                    montant_verse_total,
	                    '                ',
	                    '                    ',
	                    '000000\n']
	    for line_data_company in data_company_last:
	        f.write(str(line_data_company))

	    text = ""
	    with open("/home/odoo/virement.txt") as f:
	        content = f.readlines()
	        if content:
	            for line in content:
	                text += line

	    mdp = self.pass_crypt

	    cmd="""cd /home/odoo/
	           zip --password """+ mdp +""" virement.zip virement.txt"""

	    os.system(cmd)
	    with open("/home/odoo/virement.zip", "rb") as f:
	        fichier = f.read()
	        self.file = base64.b64encode(fichier)
	        self.name="virement.zip"
	        self.state = 'done'


	    return {
	        'name': 'Download file',
	        'context': self._context,
	        'view_type': 'form',
	        'view_mode': 'form',
	        'res_model': 'hr.payslip.virt',
	        'type': 'ir.actions.act_window',
	        'target': 'new',
	        'res_id': self[0].id,

	    }