# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BallotMeasure'
        db.create_table(u'open_ballot_ballotmeasure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('prop_id', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('election_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('num_yes', self.gf('django.db.models.fields.IntegerField')()),
            ('num_no', self.gf('django.db.models.fields.IntegerField')()),
            ('passed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ballot_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['open_ballot.BallotType'])),
        ))
        db.send_create_signal('open_ballot', ['BallotMeasure'])

        # Adding M2M table for field tags on 'BallotMeasure'
        m2m_table_name = db.shorten_name(u'open_ballot_ballotmeasure_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ballotmeasure', models.ForeignKey(orm['open_ballot.ballotmeasure'], null=False)),
            ('tag', models.ForeignKey(orm['open_ballot.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ballotmeasure_id', 'tag_id'])

        # Adding model 'BallotType'
        db.create_table(u'open_ballot_ballottype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('percent_required', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=2)),
        ))
        db.send_create_signal('open_ballot', ['BallotType'])

        # Adding model 'Tag'
        db.create_table(u'open_ballot_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('open_ballot', ['Tag'])

        # Adding model 'Committee'
        db.create_table(u'open_ballot_committee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('filer_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('open_ballot', ['Committee'])

        # Adding unique constraint on 'Committee', fields ['name', 'filer_id']
        db.create_unique(u'open_ballot_committee', ['name', 'filer_id'])

        # Adding model 'Stance'
        db.create_table(u'open_ballot_stance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('voted_yes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['open_ballot.Committee'])),
            ('ballot_measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['open_ballot.BallotMeasure'])),
        ))
        db.send_create_signal('open_ballot', ['Stance'])

        # Adding unique constraint on 'Stance', fields ['committee', 'ballot_measure']
        db.create_unique(u'open_ballot_stance', ['committee_id', 'ballot_measure_id'])

        # Adding model 'Consultant'
        db.create_table(u'open_ballot_consultant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('open_ballot', ['Consultant'])

        # Adding model 'Contract'
        db.create_table(u'open_ballot_contract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('payment', self.gf('django.db.models.fields.FloatField')()),
            ('consultant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['open_ballot.Consultant'])),
            ('service', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['open_ballot.Service'], unique=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['open_ballot.Committee'])),
        ))
        db.send_create_signal('open_ballot', ['Contract'])

        # Adding model 'Service'
        db.create_table(u'open_ballot_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('open_ballot', ['Service'])

        # Adding model 'Donor'
        db.create_table(u'open_ballot_donor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['open_ballot.Employer'], null=True)),
        ))
        db.send_create_signal('open_ballot', ['Donor'])

        # Adding unique constraint on 'Donor', fields ['first_name', 'last_name', 'latitude', 'longitude']
        db.create_unique(u'open_ballot_donor', ['first_name', 'last_name', 'latitude', 'longitude'])

        # Adding model 'Employer'
        db.create_table(u'open_ballot_employer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('open_ballot', ['Employer'])

        # Adding model 'Donation'
        db.create_table(u'open_ballot_donation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('transaction_date', self.gf('django.db.models.fields.DateField')()),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['open_ballot.Donor'])),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['open_ballot.Committee'])),
        ))
        db.send_create_signal('open_ballot', ['Donation'])


    def backwards(self, orm):
        # Removing unique constraint on 'Donor', fields ['first_name', 'last_name', 'latitude', 'longitude']
        db.delete_unique(u'open_ballot_donor', ['first_name', 'last_name', 'latitude', 'longitude'])

        # Removing unique constraint on 'Stance', fields ['committee', 'ballot_measure']
        db.delete_unique(u'open_ballot_stance', ['committee_id', 'ballot_measure_id'])

        # Removing unique constraint on 'Committee', fields ['name', 'filer_id']
        db.delete_unique(u'open_ballot_committee', ['name', 'filer_id'])

        # Deleting model 'BallotMeasure'
        db.delete_table(u'open_ballot_ballotmeasure')

        # Removing M2M table for field tags on 'BallotMeasure'
        db.delete_table(db.shorten_name(u'open_ballot_ballotmeasure_tags'))

        # Deleting model 'BallotType'
        db.delete_table(u'open_ballot_ballottype')

        # Deleting model 'Tag'
        db.delete_table(u'open_ballot_tag')

        # Deleting model 'Committee'
        db.delete_table(u'open_ballot_committee')

        # Deleting model 'Stance'
        db.delete_table(u'open_ballot_stance')

        # Deleting model 'Consultant'
        db.delete_table(u'open_ballot_consultant')

        # Deleting model 'Contract'
        db.delete_table(u'open_ballot_contract')

        # Deleting model 'Service'
        db.delete_table(u'open_ballot_service')

        # Deleting model 'Donor'
        db.delete_table(u'open_ballot_donor')

        # Deleting model 'Employer'
        db.delete_table(u'open_ballot_employer')

        # Deleting model 'Donation'
        db.delete_table(u'open_ballot_donation')


    models = {
        'open_ballot.ballotmeasure': {
            'Meta': {'object_name': 'BallotMeasure'},
            'ballot_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['open_ballot.BallotType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'election_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'num_no': ('django.db.models.fields.IntegerField', [], {}),
            'num_yes': ('django.db.models.fields.IntegerField', [], {}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prop_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['open_ballot.Tag']", 'symmetrical': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.ballottype': {
            'Meta': {'object_name': 'BallotType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'percent_required': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.committee': {
            'Meta': {'unique_together': "(('name', 'filer_id'),)", 'object_name': 'Committee'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'filer_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.consultant': {
            'Meta': {'object_name': 'Consultant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.contract': {
            'Meta': {'object_name': 'Contract'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['open_ballot.Committee']"}),
            'consultant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['open_ballot.Consultant']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.FloatField', [], {}),
            'service': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['open_ballot.Service']", 'unique': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.donation': {
            'Meta': {'object_name': 'Donation'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['open_ballot.Committee']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['open_ballot.Donor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction_date': ('django.db.models.fields.DateField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.donor': {
            'Meta': {'unique_together': "(('first_name', 'last_name', 'latitude', 'longitude'),)", 'object_name': 'Donor'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['open_ballot.Employer']", 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.employer': {
            'Meta': {'object_name': 'Employer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.service': {
            'Meta': {'object_name': 'Service'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'open_ballot.stance': {
            'Meta': {'unique_together': "(('committee', 'ballot_measure'),)", 'object_name': 'Stance'},
            'ballot_measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['open_ballot.BallotMeasure']"}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['open_ballot.Committee']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'voted_yes': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'open_ballot.tag': {
            'Meta': {'object_name': 'Tag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['open_ballot']