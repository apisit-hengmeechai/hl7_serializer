from rest_framework import serializers
from snippets.models import PatientOrganization, Patient, PatientIdentifier, PatientCommunication, PatientName, PatientAddress, PatientContact

class PatientIdentifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientIdentifier
        fields = ('type', 'value', 'facility', 'start', 'end')
    '''
    def create(self, patient, validated_data):
        pid = PatientIdentifier.objects.create(patient=patient, type=validated_data['type'], value=validated_data['value'], facility=validated_data['facility'], start=validated_data['start'], end=validated_data['end'])
        return pid
    '''

class PatientNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientName
        fields = ('prefix', 'given_name', 'middle_name', 'family_name', 'suffix', 'language')


class PatientCommunicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientCommunication
        fields = ('language', 'preferred')

class PatientAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientAddress
        fields = ('line','city','district','state','country','postcode')
    
class PatientContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PatientContact
        fields = ('system', 'use', 'value')

class PatientOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientOrganization
        fields = ('code_name','code_number','name')
    
    def create(self, validated_data):
        return PatientOrganization.objects.create(**validated_data)

class PatientSerializer(serializers.ModelSerializer):
    resource_type = serializers.ReadOnlyField()
    identifier = PatientIdentifierSerializer(many=True, source='identifier_set')
    name = PatientNameSerializer(many=True, source='name_set')
    communication = PatientCommunicationSerializer(many=True, source='communication_set')
    address = PatientAddressSerializer(many=True, source='address_set')
    contact = PatientContactSerializer(many=True, source='contact_set')
    organization = PatientOrganizationSerializer(many=False)

    class Meta:
        model = Patient
        fields = ('resource_type', 'id', 'row_id', 'identifier', 'name', 'gender', 'birth_date', 'nationality', 'religion' ,'communication', 'address', 'deceased', 'deceased_datetime', 'marital_status', 'contact', 'organization')
    
    def create(self, validated_data):
        def AddPatient(Data):
            Data
            return list(map(get_iden, PatientIdentifier.objects.all()))
        #validated_data['organization']
        ou = validated_data['organization']
        ou_ser = PatientOrganizationSerializer(data=ou)
        if ou_ser.is_valid():
            ou_ser_ins = ou_ser.save()
            validated_data['organization'] = ou_ser_ins

            

            identifier_data = validated_data.pop('identifier_set')
            name_data = validated_data.pop('name_set')
            communication_data = validated_data.pop('communication_set')
            address_data = validated_data.pop('address_set')
            contact_data = validated_data.pop('contact_set')

            patient = Patient.objects.create(**validated_data)

            list(map(lambda x : x.update({'patient':patient}), identifier_data))
            list(map(lambda x : x.update({'patient':patient}), name_data))
            list(map(lambda x : x.update({'patient':patient}), communication_data))
            list(map(lambda x : x.update({'patient':patient}), address_data))
            list(map(lambda x : x.update({'patient':patient}), contact_data))

            list(map(lambda x : PatientIdentifier.objects.create(**x), identifier_data))
            list(map(lambda x : PatientName.objects.create(**x), name_data))
            list(map(lambda x : PatientCommunication.objects.create(**x), communication_data))
            list(map(lambda x : PatientAddress.objects.create(**x), address_data))
            list(map(lambda x : PatientContact.objects.create(**x), contact_data))

            #identifier_data['patient'] = patient
            #name_data['patient'] = patient
            #communication_data['patient'] = patient
            #address_data['patient'] = patient
            #contact_data['patient'] = patient

            #PatientIdentifier.objects.create(**identifier_data, many=True)
            #PatientName.objects.create(**name_data, many=True)
            #PatientCommunication.objects.create(**communication_data, many=True)
            #PatientAddress.objects.create(**address_data, many=True)
            #PatientContact.objects.create(**contact_data, many=True)


        return patient
    
    def __str__(self):
        try:
            return self.identifier_set.get(type='MRN').value
        except:
            return str(self.id)