# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('lifetime_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('lifetime', ['Category'])

        # Adding model 'Supply'
        db.create_table('lifetime_supply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('lifetime', ['Supply'])

        # Adding M2M table for field categories on 'Supply'
        db.create_table('lifetime_supply_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('supply', models.ForeignKey(orm['lifetime.supply'], null=False)),
            ('category', models.ForeignKey(orm['lifetime.category'], null=False))
        ))
        db.create_unique('lifetime_supply_categories', ['supply_id', 'category_id'])

        # Adding model 'Subscription'
        db.create_table('lifetime_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('supply', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscription', to=orm['lifetime.Supply'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('length_days', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('lifetime', ['Subscription'])

        # Adding model 'Product'
        db.create_table('lifetime_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('img', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lifetime', ['Product'])

        # Adding M2M table for field categories on 'Product'
        db.create_table('lifetime_product_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['lifetime.product'], null=False)),
            ('category', models.ForeignKey(orm['lifetime.category'], null=False))
        ))
        db.create_unique('lifetime_product_categories', ['product_id', 'category_id'])

        # Adding model 'ProductDetail'
        db.create_table('lifetime_productdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lifetime.Product'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('lifetime', ['ProductDetail'])

        # Adding model 'Gift'
        db.create_table('lifetime_gift', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supply', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lifetime.Supply'], null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(default='e0XgrNVp', unique=True, max_length=8)),
        ))
        db.send_create_signal('lifetime', ['Gift'])

        # Adding model 'Order'
        db.create_table('lifetime_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supply', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lifetime.Supply'])),
            ('date_placed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_shipped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('item_quanity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('lifetime', ['Order'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('lifetime_category')

        # Deleting model 'Supply'
        db.delete_table('lifetime_supply')

        # Removing M2M table for field categories on 'Supply'
        db.delete_table('lifetime_supply_categories')

        # Deleting model 'Subscription'
        db.delete_table('lifetime_subscription')

        # Deleting model 'Product'
        db.delete_table('lifetime_product')

        # Removing M2M table for field categories on 'Product'
        db.delete_table('lifetime_product_categories')

        # Deleting model 'ProductDetail'
        db.delete_table('lifetime_productdetail')

        # Deleting model 'Gift'
        db.delete_table('lifetime_gift')

        # Deleting model 'Order'
        db.delete_table('lifetime_order')


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
        'lifetime.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lifetime.gift': {
            'Meta': {'object_name': 'Gift'},
            'code': ('django.db.models.fields.CharField', [], {'default': "'hShFi0z0'", 'unique': 'True', 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lifetime.Supply']", 'null': 'True', 'blank': 'True'})
        },
        'lifetime.order': {
            'Meta': {'object_name': 'Order'},
            'date_placed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_shipped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_quanity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'supply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lifetime.Supply']"})
        },
        'lifetime.product': {
            'Meta': {'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lifetime.Category']", 'symmetrical': 'False'}),
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
            'supply': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscription'", 'to': "orm['lifetime.Supply']"})
        },
        'lifetime.supply': {
            'Meta': {'object_name': 'Supply'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lifetime.Category']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['lifetime']