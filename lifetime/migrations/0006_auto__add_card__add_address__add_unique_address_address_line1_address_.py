# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Card'
        db.create_table('lifetime_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('stripe_id', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('card_type', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('last4', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('lifetime', ['Card'])

        # Adding model 'Address'
        db.create_table('lifetime_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_obj', unique=True, null=True, to=orm['auth.User'])),
            ('address_line1', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('address_line2', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country', self.gf('django.db.models.fields.CharField')(default='USA', max_length=40, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('edited', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lifetime', ['Address'])

        # Adding unique constraint on 'Address', fields ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country']
        db.create_unique('lifetime_address', ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'])

        # Adding model 'GiftModel'
        db.create_table('lifetime_giftmodel', (
            ('subscription_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lifetime.Subscription'], unique=True, primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gift', null=True, to=orm['lifetime.Subscription'])),
            ('code', self.gf('django.db.models.fields.CharField')(default='FFkAUKgY', unique=True, max_length=8)),
        ))
        db.send_create_signal('lifetime', ['GiftModel'])

        # Adding model 'Order'
        db.create_table('lifetime_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lifetime.Subscription'])),
            ('date_placed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_shipped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('shipped', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('item_quanity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('lifetime', ['Order'])

        # Adding model 'ProductDetails'
        db.create_table('lifetime_productdetails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lifetime.Product'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('lifetime', ['ProductDetails'])

        # Adding model 'Subscription'
        db.create_table('lifetime_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lifetime.Product'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('length_days', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('lifetime', ['Subscription'])


    def backwards(self, orm):
        # Removing unique constraint on 'Address', fields ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country']
        db.delete_unique('lifetime_address', ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'])

        # Deleting model 'Card'
        db.delete_table('lifetime_card')

        # Deleting model 'Address'
        db.delete_table('lifetime_address')

        # Deleting model 'GiftModel'
        db.delete_table('lifetime_giftmodel')

        # Deleting model 'Order'
        db.delete_table('lifetime_order')

        # Deleting model 'ProductDetails'
        db.delete_table('lifetime_productdetails')

        # Deleting model 'Subscription'
        db.delete_table('lifetime_subscription')


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
        'lifetime.address': {
            'Meta': {'unique_together': "(('address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'),)", 'object_name': 'Address'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'USA'", 'max_length': '40', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_obj'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'lifetime.card': {
            'Meta': {'object_name': 'Card'},
            'card_type': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last4': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'stripe_id': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50'}),
            'token': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50'})
        },
        'lifetime.giftmodel': {
            'Meta': {'object_name': 'GiftModel', '_ormbases': ['lifetime.Subscription']},
            'code': ('django.db.models.fields.CharField', [], {'default': "'iQI129Gy'", 'unique': 'True', 'max_length': '8'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gift'", 'null': 'True', 'to': "orm['lifetime.Subscription']"}),
            'subscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lifetime.Subscription']", 'unique': 'True', 'primary_key': 'True'})
        },
        'lifetime.order': {
            'Meta': {'object_name': 'Order'},
            'date_placed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_shipped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_quanity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shipped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'lifetime.productdetails': {
            'Meta': {'object_name': 'ProductDetails'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lifetime.Product']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'lifetime.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lifetime.Product']"}),
            'total_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'lifetime.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prefered_card': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['lifetime']