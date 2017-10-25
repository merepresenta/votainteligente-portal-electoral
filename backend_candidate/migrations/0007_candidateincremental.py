# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-23 21:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0030_election_candidates_can_commit_everywhere'),
        ('backend_candidate', '0006_proposalsuggestionforincremental_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateIncremental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Candidate')),
                ('suggestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_candidate.IncrementalsCandidateFilter')),
            ],
        ),
    ]
