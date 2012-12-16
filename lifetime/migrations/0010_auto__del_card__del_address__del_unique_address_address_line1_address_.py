# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Address', fields ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country']
        db.delete_unique('lifetime_address', ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'])

        # Deleting model 'Card'
        db.delete_table('lifetime_card')

        # Deleting model 'Address'
        db.delete_table('lifetime_address')

        # Deleting model 'UserProfile'
        db.delete_table('lifetime_userprofile')

        # Deleting field 'Order.shipped'
        db.delete_column('lifetime_order', 'shipped')


    def backwards(self, orm):
        # Adding model 'Card'
        db.create_table('lifetime_card', (
            ('card_type', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('last4', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('token', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('stripe_id', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lifetime', ['Card'])

        # Adding model 'Address'
        db.create_table('lifetime_address', (
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('edited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address_line2', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address_line1', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('country', self.gf('django.db.models.fields.CharField')(default='USA', max_length=40, blank=True)),
        ))
        db.send_create_signal('lifetime', ['Address'])

        # Adding unique constraint on 'Address', fields ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country']
        db.create_unique('lifetime_address', ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'])

        # Adding model 'UserProfile'
        db.create_table('lifetime_userprofile', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefered_card', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('lifetime', ['UserProfile'])

        # Adding field 'Order.shipped'
        db.add_column('lifetime_order', 'shipped',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lifetime.giftmodel': {
            'Meta': {'object_name': 'GiftModel', '_ormbases': ['lifetime.Subscription']},
            'code': ('django.db.models.fields.CharField', [], {'default': "'rZZXWe1J'", 'unique': 'True', 'max_length': '8'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gift'", 'null': 'True', 'to': "orm['lifetime.Subscription']"}),
            'subscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lifetime.Subscription']", 'unique': 'True', 'primary_key': 'True'})
        },
        'lifetime.order': {
            'Meta': {'object_name': 'Order'},
            'date_placed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_shipped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_quanity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lifetime.Subscription']"})
        },
        'lifetime.product': {
            'Meta': {'object_name': 'Product'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        'lifetime.productdetail': {
            'Meta': {'object_name': 'ProductDetail'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lifetime.Product']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'lifetime.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lifetime.Product']"}),
            'total_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['lifetime']