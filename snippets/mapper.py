import requests

class PatientJson():
    def __init__(self):
        self.pasid = input("Enter Patient ID: ")
    
    def _get_raw_patient_json(self):
        query_string = "SELECT top 10 CASE WHEN rf_type.ValueCode = 'NATID' THEN 'NID' WHEN rf_type.ValueCode = 'PASID' THEN 'MRN' WHEN rf_type.ValueCode = 'PSPNM' THEN 'PPN' ELSE 'TMP' END type, CASE WHEN pid.identifier IS NOT NULL OR LEN(pid.identifier) > 1 THEN pid.identifier ELSE NULL END 'value','048' facility, pid.activefrom 'start', pid.activeto 'end', NULL suffix, rf_title.description, CASE WHEN p.middlename = '' THEN NULL ELSE p.middlename END middle_name, p.surname family_name, p.forename given_name, rf_commu.valuecode, CASE WHEN addr.CITTYUID IS NOT NULL THEN ( SELECT TOP 1 Description FROM dbo.ReferenceValue WHERE UID = addr.CITTYUID) ELSE NULL END district, isnull(addr.line1,'') + ' ' + isnull(addr.line2,'') + ' ' + isnull(addr.line3,'') + ' ' + isnull(addr.line4,'') line, CASE WHEN addr.STATEUID IS NOT NULL THEN ( SELECT TOP 1 Description FROM dbo.ReferenceValue WHERE UID = addr.STATEUID) ELSE NULL END state_desc,  CASE WHEN addr.CNTRYUID IS NOT NULL THEN ( SELECT TOP 1 ValueCode FROM dbo.ReferenceValue WHERE UID = addr.CNTRYUID) ELSE NULL END country, CASE WHEN addr.Pincode='999999' THEN NULL ELSE addr.Pincode END zipcode, CASE WHEN addr.AREAUID IS NOT NULL THEN ( SELECT TOP 1 Description FROM ReferenceValue WHERE UID = addr.AREAUID) ELSE NULL END city, rf_commu.valuecode commu_language, CASE WHEN rf_commu.statusflag = 'A' THEN 'True' ELSE 'False' END preferred, CASE WHEN poc.cntypuid = 1 THEN 'phone' WHEN poc.cntypuid = 2 THEN 'phone' WHEN poc.cntypuid = 3 THEN 'email' ELSE NULL END system, RTRIM(LTRIM(REPLACE( poc.line1 , '-' , '' ))) contact_value, (SELECT TOP 1 description FROM referencevalue WHERE uid = p.VIPTPUID AND StatusFlag = 'A') vip_type, p.registrationdttm, '48-' + CAST(p.uid AS VARCHAR) row_id, CAST(p.BirthDttm AS DATE) birth_date, CASE WHEN pdd.uid IS NOT NULL THEN 'True' ELSE 'False' END deceased, CASE WHEN p.SEXXXUID = '55631' THEN 'F' WHEN p.SEXXXUID = '55630' THEN 'M' ELSE NULL END gender, CASE WHEN(pdd.DeathDttm IS NOT NULL) AND(pdd.DeathTime IS NOT NULL) THEN(CAST(CONVERT(CHAR(10), pdd.DeathDttm, 126) + ' ' + SUBSTRING(CONVERT(CHAR(20), pdd.deathTime, 126), 12, 8) AS DATETIME)) ELSE NULL END deceased_datetime, rf_nation.ValueCode nationality, rf_reli.description religion, CASE WHEN p.MARRYUID IS NULL OR p.MARRYUID = '0' THEN 'Unknown' ELSE rf_marital.Description END marital_status, '048' code_number, 'BKN' code_name, 'Bangkok Hospital Khon Kaen' name, p.pasid FROM Patient p LEFT JOIN ReferenceValue rf_nation ON rf_nation.uid = p.NATNLUID LEFT JOIN PatientDeceasedDetail pdd ON pdd.patientuid = p.uid LEFT JOIN ReferenceValue rf_reli ON rf_reli.uid = p.RELGNUID LEFT JOIN referencevalue rf_marital ON rf_marital.uid = p.MARRYUID LEFT JOIN ReferenceValue rf_title ON rf_title.uid = p.titleuid LEFT JOIN ReferenceValue rf_commu ON rf_commu.uid = p.spokluid LEFT JOIN PatientID pid ON pid.patientuid = p.uid AND pid.statusflag = 'A' LEFT JOIN ReferenceValue rf_type ON rf_type.uid = pid.pitypuid LEFT JOIN patientaddress addr ON addr.patientuid = p.uid LEFT JOIN PatientOtherContact poc ON poc.patientuid = p.uid AND poc.statusflag = 'A' AND poc.line1 <> '' WHERE pid.identifier <> '' AND p.pasid = '{0}'".format(self.pasid)
        data = requests.post('http://localhost:10011/new/his_b-connect', query_string)
        return data.json()

    def _arrange_patient_json(self, data):
        dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])

        patient = dictfilt(data, [ "row_id", "birth_date", "deceased", "deceased_datetime", "gender", "nationality", "religion", "marital_status"] )
        patient['resource_type'] = 'Patient'
        patient['identifier'] = dictfilt(data, ( "type", "value", "facility", "start", "end" ))
        patient['name'] = dictfilt(data, ( "suffix", "description", "middle_name", "family_name", "given_name", "valuecode" ))
        patient['address'] = dictfilt(data, ( "district", "line", "state_desc", "country", "zipcode", "city" ))
        patient['communication'] = dictfilt(data, ( "commu_language", "preferred" ))
        patient['communication']['language'] = patient['communication'].pop('commu_language')
        patient['contact'] = dictfilt(data, ( "system", "contact_value" ))
        patient['contact']['value'] = patient['contact'].pop('contact_value')
        patient['organization'] = dictfilt(data, ( "code_number", "code_name", "name" ))
        return patient

    def _merge_patient(self, patient_json):
        data = self._get_raw_patient_json()
        patient_template =  {
            "resource_type" : "Patient",
            "row_id" : "",
            "identifier" : [],
            "name" : [],
            "gender" : "",
            "birth_date" : "",
            "nationality" : "",
            "religion" : "",
            "communication" : [],
            "address" : [],
            "deceased" : "",
            "deceased_datetime" : "",
            "marital_status" : "",
            "contact" : [],
            "organization" : {}
        }
        key = ['identifier', 'name', 'communication', 'address', 'contact']
        #patient_template.update(patient_json[0])
        data = list( map( (lambda x: patient_template['identifier'].append(x['identifier']) if x['identifier'] not in patient_template['identifier'] else None ) ,patient_json) )
        data = list( map( (lambda x: patient_template['name'].append(x['name']) if x['name'] not in patient_template['name'] else None ) ,patient_json) )
        data = list( map( (lambda x: patient_template['communication'].append(x['communication']) if x['communication'] not in patient_template['communication'] else None ) ,patient_json) )
        data = list( map( (lambda x: patient_template['address'].append(x['address']) if x['address'] not in patient_template['address'] else None ) ,patient_json) )
        data = list( map( (lambda x: patient_template['contact'].append(x['contact']) if x['contact'] not in patient_template['contact'] else None ) ,patient_json) )
        list( map( (lambda x: patient_json[0].pop(x)), key ) )
        patient_template = dict(patient_template, **patient_json[0])
        return patient_template


    def _get_patient_json(self):
        patient_json = list(map(self._arrange_patient_json, self._get_raw_patient_json()))
        out = self._merge_patient(patient_json)
        return out