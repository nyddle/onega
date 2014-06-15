# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table(u'chips_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('post_index', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('corpus', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('apartment', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('banks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blocks_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'chips', ['Customer'])

        # Adding M2M table for field groups on 'Customer'
        m2m_table_name = db.shorten_name(u'chips_customer_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm[u'chips.customer'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customer_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Customer'
        m2m_table_name = db.shorten_name(u'chips_customer_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm[u'chips.customer'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customer_id', 'permission_id'])

        # Adding model 'SiteSettings'
        db.create_table(u'chips_sitesettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('additional_data', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'chips', ['SiteSettings'])

        # Adding model 'ValidCode'
        db.create_table(u'chips_validcode', (
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, primary_key=True)),
        ))
        db.send_create_signal(u'chips', ['ValidCode'])

        # Adding model 'ImageGallery'
        db.create_table(u'chips_imagegallery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'chips', ['ImageGallery'])

        # Adding model 'Phase'
        db.create_table(u'chips_phase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_phase', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'chips', ['Phase'])

        # Adding model 'PriseType'
        db.create_table(u'chips_prisetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'chips', ['PriseType'])

        # Adding model 'PromoCode'
        db.create_table(u'chips_promocode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chips.Customer'])),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('winner', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('on_phase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chips.Phase'], null=True, blank=True)),
            ('prise_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chips.PriseType'], null=True, blank=True)),
        ))
        db.send_create_signal(u'chips', ['PromoCode'])

        # Adding model 'WrongCode'
        db.create_table(u'chips_wrongcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chips.Customer'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'chips', ['WrongCode'])

        # Adding model 'DiscreditedIP'
        db.create_table(u'chips_discreditedip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('failed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blocked', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'chips', ['DiscreditedIP'])

        # Adding model 'WrongIPByCode'
        db.create_table(u'chips_wrongipbycode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chips.DiscreditedIP'])),
        ))
        db.send_create_signal(u'chips', ['WrongIPByCode'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table(u'chips_customer')

        # Removing M2M table for field groups on 'Customer'
        db.delete_table(db.shorten_name(u'chips_customer_groups'))

        # Removing M2M table for field user_permissions on 'Customer'
        db.delete_table(db.shorten_name(u'chips_customer_user_permissions'))

        # Deleting model 'SiteSettings'
        db.delete_table(u'chips_sitesettings')

        # Deleting model 'ValidCode'
        db.delete_table(u'chips_validcode')

        # Deleting model 'ImageGallery'
        db.delete_table(u'chips_imagegallery')

        # Deleting model 'Phase'
        db.delete_table(u'chips_phase')

        # Deleting model 'PriseType'
        db.delete_table(u'chips_prisetype')

        # Deleting model 'PromoCode'
        db.delete_table(u'chips_promocode')

        # Deleting model 'WrongCode'
        db.delete_table(u'chips_wrongcode')

        # Deleting model 'DiscreditedIP'
        db.delete_table(u'chips_discreditedip')

        # Deleting model 'WrongIPByCode'
        db.delete_table(u'chips_wrongipbycode')


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
        u'chips.discreditedip': {
            'Meta': {'object_name': 'DiscreditedIP'},
            'blocked': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'failed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'chips.imagegallery': {
            'Meta': {'object_name': 'ImageGallery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'chips.phase': {
            'Meta': {'object_name': 'Phase'},
            'current_phase': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'on_phase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chips.Phase']", 'null': 'True', 'blank': 'True'}),
            'prise_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chips.PriseType']", 'null': 'True', 'blank': 'True'}),
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
        u'chips.wrongipbycode': {
            'Meta': {'object_name': 'WrongIPByCode'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chips.DiscreditedIP']"})
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