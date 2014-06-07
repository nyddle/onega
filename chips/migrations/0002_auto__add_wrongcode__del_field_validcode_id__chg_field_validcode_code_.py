# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WrongCode'
        db.create_table(u'chips_wrongcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chips.Customer'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'chips', ['WrongCode'])

        # Deleting field 'ValidCode.id'
        db.delete_column(u'chips_validcode', u'id')


        # Changing field 'ValidCode.code'
        db.alter_column(u'chips_validcode', 'code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, primary_key=True))
        # Deleting field 'Customer.blocked_at'
        db.delete_column(u'chips_customer', 'blocked_at')

        # Adding field 'Customer.blocks_count'
        db.add_column(u'chips_customer', 'blocks_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'WrongCode'
        db.delete_table(u'chips_wrongcode')


        # User chose to not deal with backwards NULL issues for 'ValidCode.id'
        raise RuntimeError("Cannot reverse this migration. 'ValidCode.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ValidCode.id'
        db.add_column(u'chips_validcode', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


        # Changing field 'ValidCode.code'
        db.alter_column(u'chips_validcode', 'code', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True))
        # Adding field 'Customer.blocked_at'
        db.add_column(u'chips_customer', 'blocked_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Customer.blocks_count'
        db.delete_column(u'chips_customer', 'blocks_count')


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
        u'chips.customer': {
            'Meta': {'object_name': 'Customer'},
            'apartment': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'banks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blocks_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'corpus': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'post_index': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'chips.imagegallery': {
            'Meta': {'object_name': 'ImageGallery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'chips.phase': {
            'Meta': {'object_name': 'Phase'},
            'current_phase': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'chips.prisetype': {
            'Meta': {'object_name': 'PriseType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'chips.promocode': {
            'Meta': {'object_name': 'PromoCode'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chips.Customer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_phase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chips.Phase']", 'null': 'True'}),
            'prise_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chips.PriseType']", 'null': 'True'}),
            'winner': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'chips.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'additional_data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'chips.validcode': {
            'Meta': {'object_name': 'ValidCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'primary_key': 'True'})
        },
        u'chips.wrongcode': {
            'Meta': {'object_name': 'WrongCode'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chips.Customer']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chips']