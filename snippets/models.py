from django.db import models
import uuid
#from snippets.serializers import PatientIdentifierSerializer

class PatientOrganization(models.Model):
    code_name = models.CharField(max_length=20)
    code_number = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    @property
    def resource_type(self):
        return 'Organization'

    def __str__(self):
        return self.name

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    row_id = models.CharField(max_length=100, null=True, default=None, unique=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    deceased = models.BooleanField(default=False)
    deceased_datetime = models.DateTimeField(null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(max_length=100, null=True, blank=True)
    organization = models.ForeignKey(PatientOrganization, related_name='patient_org', on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def resource_type(self):
        return 'Patient'

    def __str__(self):
        try:
            return self.identifier_set.get(type='MRN').value
        except:
            return str(self.id)

class PatientIdentifier(models.Model):
    patient = models.ForeignKey(Patient, related_name='identifier_set', on_delete=models.CASCADE)
    type = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    facility = models.CharField(max_length=100)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    
    @property
    def resource_type(self):
        return 'Identifier'


class PatientCommunication(models.Model):
    patient = models.ForeignKey(Patient, related_name='communication_set', on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    preferred = models.BooleanField(default=False)

    @property
    def resource_type(self):
        return 'Communication'

class PatientName(models.Model):
    patient = models.ForeignKey(Patient, related_name='name_set', on_delete=models.CASCADE)
    prefix = models.CharField(max_length=100, blank=True, null=True)
    given_name = models.CharField(max_length=100, db_index=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    family_name = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    suffix = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    
    @property
    def resource_type(self):
        return 'Name'

class PatientAddress(models.Model):
    patient = models.ForeignKey(Patient, related_name='address_set', on_delete=models.CASCADE)
    line = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    
    @property
    def resource_type(self):
        return 'Address'

class PatientContact(models.Model):
    patient = models.ForeignKey(Patient, related_name='contact_set', on_delete=models.CASCADE)
    system = models.CharField(max_length=100)
    use = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=100)

    @property
    def resource_type(self):
        return 'Contact'