from django.db import models

class files(models.Model):
    class Meta:
        db_table = 'files'  

    id = models.AutoField(primary_key=True)
    input_file_name=models.CharField(max_length=500,blank=False)
    output_file_name=models.CharField(max_length=500,blank=False)
    transaction_time=models.DateTimeField(auto_now_add=True)

    def savedata(self):
        self.save()

    def __str__(self):
        return self.input_file_name+'-'+self.output_file_name  

class financial_data(models.Model):
    ''' model for financial data to be store in db'''
    class Meta:
        db_table = 'financial_data' 

    id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=500)
    field_name = models.CharField(max_length=500)
    field_value =  models.IntegerField()
    year = models.IntegerField()
    transaction_time=models.DateTimeField(auto_now_add=True)

    def savedata(self):
        self.save()

    def __str__(self):
        return '['+self.field_name+'-'+self.file+'-'+str(self.year)+'-'+str(self.field_value)+'] \n' 