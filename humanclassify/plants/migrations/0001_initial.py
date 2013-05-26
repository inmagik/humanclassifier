# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlantJudgement'
        db.create_table(u'plants_plantjudgement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('plant_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('motivation', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'plants', ['PlantJudgement'])

        # Adding model 'Plant'
        db.create_table(u'plants_plant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('offensive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('plant_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('suggested_plant_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'plants', ['Plant'])

        # Adding model 'PlantImage'
        db.create_table(u'plants_plantimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pictures', to=orm['plants.Plant'])),
            ('picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'plants', ['PlantImage'])

        # Adding model 'ReferencePlant'
        db.create_table(u'plants_referenceplant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('ordo', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('unranked_classis', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('unranked_divisio', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('regnum', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('binomial', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('familia', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('genus', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('unranked_ordo', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('binomial_authority', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'plants', ['ReferencePlant'])

        # Adding model 'ReferencePlantImage'
        db.create_table(u'plants_referenceplantimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference_plant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['plants.ReferencePlant'])),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'plants', ['ReferencePlantImage'])


    def backwards(self, orm):
        # Deleting model 'PlantJudgement'
        db.delete_table(u'plants_plantjudgement')

        # Deleting model 'Plant'
        db.delete_table(u'plants_plant')

        # Deleting model 'PlantImage'
        db.delete_table(u'plants_plantimage')

        # Deleting model 'ReferencePlant'
        db.delete_table(u'plants_referenceplant')

        # Deleting model 'ReferencePlantImage'
        db.delete_table(u'plants_referenceplantimage')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'judgements.judgement': {
            'Meta': {'object_name': 'Judgement'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'fieldname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motivation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('jsonfield.fields.JSONField', [], {'default': '{}'})
        },
        u'plants.plant': {
            'Meta': {'object_name': 'Plant'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'offensive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'plant_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'suggested_plant_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'plants.plantimage': {
            'Meta': {'object_name': 'PlantImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'plant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pictures'", 'to': u"orm['plants.Plant']"})
        },
        u'plants.plantjudgement': {
            'Meta': {'object_name': 'PlantJudgement'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motivation': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'plant_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'plants.referenceplant': {
            'Meta': {'ordering': "['name', 'genus']", 'object_name': 'ReferencePlant'},
            'binomial': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'binomial_authority': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'familia': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'ordo': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'regnum': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'unranked_classis': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'unranked_divisio': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'unranked_ordo': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'plants.referenceplantimage': {
            'Meta': {'object_name': 'ReferencePlantImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'reference_plant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['plants.ReferencePlant']"})
        }
    }

    complete_apps = ['plants']