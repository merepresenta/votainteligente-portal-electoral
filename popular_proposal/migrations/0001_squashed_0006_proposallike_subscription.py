# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 16:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import djchoices.choices
import picklefield.fields


class Migration(migrations.Migration):

    replaces = [(b'popular_proposal', '0001_initial'), (b'popular_proposal', '0002_proposaltemporarydata_status'), (b'popular_proposal', '0003_auto_20160329_1622'), (b'popular_proposal', '0004_auto_20160406_2108'), (b'popular_proposal', '0005_popularproposal_title'), (b'popular_proposal', '0006_proposallike_subscription')]

    initial = True

    dependencies = [
        ('popolo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalTemporaryData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', picklefield.fields.PickledObjectField(editable=False)),
                ('rejected', models.BooleanField(default=False)),
                ('rejected_reason', models.TextField()),
                ('comments', picklefield.fields.PickledObjectField(editable=False)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_proposals', to='popolo.Area')),
                ('organization', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temporary_proposals', to='popolo.Organization')),
                ('proposer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_proposals', to=settings.AUTH_USER_MODEL)),
                ('status', models.CharField(choices=[('in_our_side', b'InOurSide')], default='in_our_side', max_length=16, validators=[djchoices.choices.ChoicesValidator({'in_our_side': b'InOurSide'})])),
            ],
        ),
        migrations.CreateModel(
            name='PopularProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', picklefield.fields.PickledObjectField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='popolo.Area')),
                ('proposer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelManagers(
            name='proposaltemporarydata',
            managers=[
                ('needing_moderation', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='proposaltemporarydata',
            name='status',
            field=models.CharField(choices=[('in_our_side', b'InOurSide'), ('in_their_side', b'InTheirSide'), ('rejected', b'Rejected')], default='in_our_side', max_length=16, validators=[djchoices.choices.ChoicesValidator({'in_our_side': b'InOurSide', 'in_their_side': b'InTheirSide', 'rejected': b'Rejected'})]),
        ),
        migrations.AddField(
            model_name='popularproposal',
            name='temporary',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_proposal', to='popular_proposal.ProposalTemporaryData'),
        ),
        migrations.AlterField(
            model_name='proposaltemporarydata',
            name='status',
            field=models.CharField(choices=[('in_our_side', b'InOurSide'), ('in_their_side', b'InTheirSide'), ('rejected', b'Rejected'), ('accepted', b'Accepted')], default='in_our_side', max_length=16, validators=[djchoices.choices.ChoicesValidator({'accepted': b'Accepted', 'in_our_side': b'InOurSide', 'in_their_side': b'InTheirSide', 'rejected': b'Rejected'})]),
        ),
        migrations.AddField(
            model_name='popularproposal',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.CreateModel(
            name='ProposalLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='popular_proposal.PopularProposal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('proposal_like', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='popular_proposal.ProposalLike')),
            ],
        ),
    ]
