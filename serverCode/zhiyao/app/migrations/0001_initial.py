# Generated by Django 2.1.2 on 2018-10-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alterenvironment',
            fields=[
                ('alteid', models.CharField(db_column='AltEid', max_length=45, primary_key=True, serialize=False)),
                ('atime', models.DateTimeField(db_column='ATime')),
                ('atemperature', models.FloatField(blank=True, db_column='ATemperature', null=True)),
                ('ahumidity', models.FloatField(blank=True, db_column='AHumidity', null=True)),
                ('alightlntensity', models.FloatField(blank=True, db_column='ALightlntensity', null=True)),
                ('apressure', models.FloatField(blank=True, db_column='APressure', null=True)),
                ('aplantstage', models.CharField(blank=True, db_column='APlantStage', max_length=20, null=True)),
            ],
            options={
                'db_table': 'alterenvironment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Buypost',
            fields=[
                ('bid', models.CharField(db_column='BID', max_length=30, primary_key=True, serialize=False)),
                ('bplant', models.TextField(db_column='BPlant')),
                ('bdescription', models.TextField(db_column='BDescription')),
                ('bphonenum', models.CharField(db_column='BPhoneNum', max_length=11)),
                ('bprice', models.DecimalField(db_column='BPrice', decimal_places=2, max_digits=6)),
                ('releasebtime', models.DateTimeField(db_column='releaseBTime')),
            ],
            options={
                'db_table': 'buypost',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cartid', models.CharField(db_column='CartID', max_length=50, primary_key=True, serialize=False)),
                ('citemname', models.CharField(db_column='CItemName', max_length=45)),
                ('citemnum', models.IntegerField(db_column='CItemNum')),
                ('citembasicprice', models.DecimalField(db_column='CItemBasicPrice', decimal_places=2, max_digits=6)),
            ],
            options={
                'db_table': 'cart',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Commentpost',
            fields=[
                ('ctitle', models.CharField(db_column='CTitle', max_length=50)),
                ('cid', models.CharField(db_column='CID', max_length=20, primary_key=True, serialize=False)),
                ('cdescription', models.TextField(db_column='CDescription')),
                ('cimage', models.TextField(blank=True, db_column='CImage', null=True)),
                ('releasectime', models.DateTimeField(db_column='releaseCTime')),
            ],
            options={
                'db_table': 'commentpost',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Customenvironment',
            fields=[
                ('ceid', models.CharField(db_column='CEid', max_length=45, primary_key=True, serialize=False)),
                ('addtime', models.DateTimeField(db_column='addTime')),
                ('cname', models.CharField(db_column='CName', max_length=100)),
                ('cvalue', models.DecimalField(db_column='CValue', decimal_places=0, max_digits=10)),
                ('cunit', models.CharField(db_column='CUnit', max_length=10)),
                ('cplantstage', models.CharField(db_column='CPlantStage', max_length=20)),
                ('cnotes', models.TextField(blank=True, db_column='CNotes', null=True)),
            ],
            options={
                'db_table': 'customenvironment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Customstatistics',
            fields=[
                ('cstaticid', models.CharField(db_column='CStaticid', max_length=45, primary_key=True, serialize=False)),
                ('cname', models.CharField(db_column='CName', max_length=100)),
                ('csvalue', models.DecimalField(db_column='CSValue', decimal_places=0, max_digits=10)),
                ('cunit', models.CharField(db_column='CUnit', max_length=10)),
                ('notes', models.TextField(blank=True, db_column='Notes', null=True)),
            ],
            options={
                'db_table': 'customstatistics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Incubator',
            fields=[
                ('incuno', models.CharField(db_column='IncuNo', max_length=20, primary_key=True, serialize=False)),
                ('incuname', models.CharField(db_column='IncuName', max_length=45)),
                ('purchasetime', models.DateTimeField(blank=True, db_column='purchaseTime', null=True)),
            ],
            options={
                'db_table': 'incubator',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Incubatorusing',
            fields=[
                ('iuno', models.CharField(db_column='IUNo', max_length=20, primary_key=True, serialize=False)),
                ('initializetime', models.DateTimeField(db_column='initializeTime')),
                ('itemperature', models.FloatField(blank=True, db_column='ITemperature', null=True)),
                ('ihumidity', models.FloatField(blank=True, db_column='IHumidity', null=True)),
                ('ipressure', models.FloatField(blank=True, db_column='IPressure', null=True)),
                ('ilightlntensity', models.FloatField(blank=True, db_column='ILightlntensity', null=True)),
            ],
            options={
                'db_table': 'incubatorusing',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Monitorinform',
            fields=[
                ('monitorid', models.CharField(db_column='Monitorid', max_length=45, primary_key=True, serialize=False)),
                ('mtime', models.DateTimeField(db_column='MTime')),
                ('mtemperature', models.FloatField(db_column='MTemperature')),
                ('mhumidity', models.FloatField(db_column='MHumidity')),
                ('mpressure', models.FloatField(db_column='MPressure')),
                ('mlightlntensity', models.FloatField(db_column='MLightlntensity')),
                ('mplantstage', models.CharField(db_column='MPlantStage', max_length=20)),
                ('mscore', models.IntegerField(blank=True, db_column='MScore', null=True)),
            ],
            options={
                'db_table': 'monitorinform',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.CharField(db_column='orderId', max_length=50, primary_key=True, serialize=False)),
                ('odatetime', models.DateTimeField(db_column='ODateTime')),
                ('oreceivername', models.CharField(db_column='OReceiverName', max_length=45)),
                ('oaddress', models.CharField(db_column='OAddress', max_length=45)),
                ('oreceiverphon', models.CharField(db_column='OReceiverPhon', max_length=11)),
                ('ordertotalprice', models.DecimalField(blank=True, db_column='orderTotalPrice', decimal_places=2, max_digits=6, null=True)),
            ],
            options={
                'db_table': 'order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orderitem',
            fields=[
                ('orderitemid', models.CharField(db_column='orderItemId', max_length=45, primary_key=True, serialize=False)),
                ('oiname', models.CharField(db_column='OIName', max_length=50)),
                ('oinum', models.IntegerField(db_column='OINum')),
                ('oibasicprice', models.DecimalField(db_column='OIBasicPrice', decimal_places=2, max_digits=6)),
            ],
            options={
                'db_table': 'orderitem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('plantname', models.CharField(db_column='plantName', max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'plant',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Plantstatistics',
            fields=[
                ('pstaticid', models.CharField(db_column='PStaticid', max_length=45, primary_key=True, serialize=False)),
                ('plantstage', models.CharField(db_column='plantStage', max_length=20)),
                ('stemperature', models.FloatField(db_column='STemperature')),
                ('shumidity', models.FloatField(db_column='SHumidity')),
                ('spressure', models.FloatField(db_column='SPressure')),
                ('slightlntensity', models.FloatField(db_column='Slightlntensity')),
            ],
            options={
                'db_table': 'plantstatistics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productid', models.CharField(db_column='productID', max_length=20, primary_key=True, serialize=False)),
                ('productname', models.CharField(db_column='productName', max_length=45)),
                ('pdescribtion', models.TextField(blank=True, db_column='pDescribtion', null=True)),
                ('pprice', models.DecimalField(db_column='pPrice', decimal_places=2, max_digits=6)),
                ('producteddate', models.DateField(db_column='productedDate')),
                ('expirationdate', models.DateField(db_column='expirationDate')),
                ('productrepertory', models.IntegerField(db_column='productRepertory')),
                ('productunit', models.CharField(db_column='productUnit', max_length=45)),
            ],
            options={
                'db_table': 'product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Productdetail',
            fields=[
                ('pdid', models.CharField(db_column='PDid', max_length=45, primary_key=True, serialize=False)),
                ('pdname', models.CharField(db_column='PDName', max_length=45)),
                ('pdvalue', models.CharField(db_column='PDValue', max_length=45)),
                ('pdunit', models.CharField(db_column='PDUnit', max_length=45)),
                ('pdnotes', models.CharField(blank=True, db_column='PDNotes', max_length=45, null=True)),
            ],
            options={
                'db_table': 'productdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('productclass', models.CharField(db_column='productClass', max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'repository',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sellpost',
            fields=[
                ('sid', models.CharField(db_column='SID', max_length=30, primary_key=True, serialize=False)),
                ('splant', models.TextField(db_column='SPlant')),
                ('sdescription', models.TextField(db_column='SDescription')),
                ('sphonenum', models.CharField(db_column='SPhoneNum', max_length=11)),
                ('sprice', models.DecimalField(db_column='SPrice', decimal_places=2, max_digits=6)),
                ('simage', models.TextField(blank=True, db_column='SImage', null=True)),
                ('sscore', models.IntegerField(blank=True, db_column='SScore', null=True)),
                ('releasestime', models.DateTimeField(db_column='releaseSTime')),
            ],
            options={
                'db_table': 'sellpost',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.CharField(db_column='userId', max_length=45, primary_key=True, serialize=False)),
                ('userphonenum', models.CharField(db_column='userPhoneNum', max_length=11, unique=True)),
                ('usermail', models.CharField(db_column='userMail', max_length=50, unique=True)),
                ('username', models.CharField(db_column='userName', max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('userstate', models.IntegerField(db_column='userState')),
                ('registrationdate', models.DateTimeField(db_column='registrationDate')),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
