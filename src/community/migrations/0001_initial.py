# Generated by Django 3.2.12 on 2022-07-20 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegulatorCommunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locus_tag', models.CharField(help_text='The locus tag for this gene', max_length=100)),
                ('uniprot_accession', models.CharField(blank=True, help_text='The UniProt accession for this protein', max_length=50)),
                ('name', models.CharField(blank=True, help_text='The name for this gene/protein', max_length=50)),
                ('function', models.CharField(blank=True, help_text='The function for this protein', max_length=250)),
                ('description', models.TextField(blank=True, help_text='The description for this protein')),
                ('mechanism', models.CharField(choices=[('transcription factor', 'transcription factor'), ('transcription attenuator', 'transcription attenuator'), ('transcription terminator', 'transcription terminator'), ('sigma factor', 'sigma factor'), ('small rna (srna)', 'small RNA (sRNA)'), ('unknown', 'unknown')], help_text='The regulatory mechanism associated to this regulator', max_length=50)),
                ('ncbi_gene', models.CharField(blank=True, help_text='The NCBI gene identifier', max_length=50)),
                ('ncbi_protein', models.CharField(blank=True, help_text='The NCBI protein identifier', max_length=50)),
                ('genbank_accession', models.CharField(blank=True, help_text='The NCBI GenBank accession', max_length=50)),
                ('refseq_accession', models.CharField(blank=True, help_text='The NCBI RefSeq accession', max_length=50)),
                ('sequence', models.TextField(blank=True, help_text='The protein sequence for this protein')),
                ('strand', models.CharField(blank=True, choices=[('forward', 'forward'), ('reverse', 'reverse'), ('unknown', 'unknown')], help_text='The strand corresponds to the genomic coordinate forward or reverse', max_length=50)),
                ('start', models.IntegerField(blank=True, help_text='The start corresponds to the genomic coordinate of the item position in the genome sequence', null=True)),
                ('stop', models.IntegerField(blank=True, help_text='The stop corresponds to the genomic coordinate of the item position in the genome sequence', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='regulators', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Regulator',
                'verbose_name_plural': 'Regulators',
            },
        ),
        migrations.CreateModel(
            name='GeneCommunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locus_tag', models.CharField(help_text='The locus tag for this gene', max_length=100)),
                ('uniprot_accession', models.CharField(blank=True, help_text='The UniProt accession for this protein', max_length=50)),
                ('name', models.CharField(blank=True, help_text='The name for this gene/protein', max_length=50)),
                ('function', models.CharField(blank=True, help_text='The function for this protein', max_length=250)),
                ('description', models.TextField(blank=True, help_text='The description for this protein')),
                ('ncbi_gene', models.CharField(blank=True, help_text='The NCBI gene identifier', max_length=50)),
                ('ncbi_protein', models.CharField(blank=True, help_text='The NCBI protein identifier', max_length=50)),
                ('genbank_accession', models.CharField(blank=True, help_text='The NCBI GenBank accession', max_length=50)),
                ('refseq_accession', models.CharField(blank=True, help_text='The NCBI RefSeq accession', max_length=50)),
                ('sequence', models.TextField(blank=True, help_text='The protein sequence for this protein')),
                ('strand', models.CharField(blank=True, choices=[('forward', 'forward'), ('reverse', 'reverse'), ('unknown', 'unknown')], help_text='The strand corresponds to the genomic coordinate forward or reverse', max_length=50)),
                ('start', models.IntegerField(blank=True, help_text='The start corresponds to the genomic coordinate of the item position in the genome sequence', null=True)),
                ('stop', models.IntegerField(blank=True, help_text='The stop corresponds to the genomic coordinate of the item position in the genome sequence', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='genes', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Gene',
                'verbose_name_plural': 'Genes',
            },
        ),
    ]