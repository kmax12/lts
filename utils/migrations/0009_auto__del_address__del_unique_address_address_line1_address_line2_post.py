# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Address', fields ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country']
        db.delete_unique('utils_address', ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'])

        # Deleting model 'Address'
        db.delete_table('utils_address')

        # Deleting model 'Order'
        db.delete_table('utils_order')

        # Deleting model 'Card'
        db.delete_table('utils_card')

        # Deleting model 'Subscription'
        db.delete_table('utils_subscription')

        # Deleting model 'GiftModel'
        db.delete_table('utils_giftmodel')


    def backwards(self, orm):
        # Adding model 'Address'
        db.create_table('utils_address', (
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('edited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address_line2', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address_line1', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('country', self.gf('django.db.models.fields.CharField')(default='USA', max_length=40, blank=True)),
        ))
        db.send_create_signal('utils', ['Address'])

        # Adding unique constraint on 'Address', fields ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country']
        db.create_unique('utils_address', ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'])

        # Adding model 'Order'
        db.create_table('utils_order', (
            ('date_shipped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('item_quanity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_placed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('shipped', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Subscription'])),
        ))
        db.send_create_signal('utils', ['Order'])

        # Adding model 'Card'
        db.create_table('utils_card', (
            ('card_type', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('last4', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('token', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('stripe_id', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('utils', ['Card'])

        # Adding model 'Subscription'
        db.create_table('utils_subscription', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lifetime.Product'])),
            ('total_quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('length_days', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('utils', ['Subscription'])

        # Adding model 'GiftModel'
        db.create_table('utils_giftmodel', (
            ('code', self.gf('django.db.models.fields.CharField')(default=0, max_length=8)),
            ('subscription_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utils.Subscription'], unique=True, primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gift', null=True, to=orm['utils.Subscription'], blank=True)),
        ))
        db.send_create_signal('utils', ['GiftModel'])


    models = {
        
    }

    complete_apps = ['utils']