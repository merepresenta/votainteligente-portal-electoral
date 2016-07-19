# coding=utf-8
from backend_candidate.tests import SoulMateCandidateAnswerTestsBase
from elections.models import Candidate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from backend_candidate.models import Candidacy, is_candidate
from backend_candidate.forms import get_form_for_election
from django.template import Template, Context
from elections.models import Election
from candidator.models import TakenPosition


class CandidacyModelTestCase(SoulMateCandidateAnswerTestsBase):
    def setUp(self):
        super(CandidacyModelTestCase, self).setUp()
        self.feli = User.objects.get(username='feli')
        self.feli.set_password('alvarez')
        self.feli.save()
        self.candidate = Candidate.objects.get(pk=1)

    def test_instanciate_candidacy(self):
        candidacy = Candidacy.objects.create(user=self.feli,
                                             candidate=self.candidate
                                             )
        self.assertEquals(candidacy.user, self.feli)
        self.assertEquals(candidacy.candidate, self.candidate)
        self.assertTrue(candidacy.created)
        self.assertTrue(candidacy.updated)

    def test_user_has_candidacy(self):
        self.assertFalse(is_candidate(self.feli))
        candidacy = Candidacy.objects.create(user=self.feli,
                                             candidate=self.candidate
                                             )
        self.assertTrue(is_candidate(self.feli))

    def test_filter_times(self):
        template = Template("{% load votainteligente_extras %}{% if user|is_candidate %}Si{% else %}No{% endif %}")
        context = Context({'user': self.feli})
        self.assertEqual(template.render(context), u'No')
        candidacy = Candidacy.objects.create(user=self.feli,
                                             candidate=self.candidate
                                             )
        self.assertEqual(template.render(context), u'Si')

    def test_get_candidate_home(self):
        url = reverse('backend_candidate:home')
        self.client.login(username=self.feli,
                          password='alvarez')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        candidacy = Candidacy.objects.create(user=self.feli,
                                             candidate=self.candidate
                                             )
        print candidacy.candidate.id
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIn(candidacy, response.context['candidacies'])

    def test_get_complete_12_naranja(self):
        election = Election.objects.get(id=2)
        url = reverse('backend_candidate:complete_12_naranja',
                      kwargs={'slug': election.slug,
                              'candidate_id': self.candidate.id})
        self.client.login(username=self.feli,
                          password='alvarez')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        Candidacy.objects.create(user=self.feli,
                                 candidate=self.candidate
                                 )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend_candidate/complete_12_naranja.html')
        form = response.context['form']

        media_naranja_form_class = get_form_for_election(election)
        self.assertEquals(form.__class__.__name__, media_naranja_form_class.__name__)
        self.assertEquals(form.election, election)
        self.assertEquals(response.context['election'], election)
        self.assertEquals(response.context['candidate'], self.candidate)

    def test_post_complete_12_naranja(self):
        TakenPosition.objects.filter(person=self.candidate).delete()
        election = Election.objects.get(id=2)
        url = reverse('backend_candidate:complete_12_naranja',
                      kwargs={'slug': election.slug,
                              'candidate_id': self.candidate.id})
        self.client.login(username=self.feli,
                          password='alvarez')
        Candidacy.objects.create(user=self.feli,
                                 candidate=self.candidate
                                 )
        data = self.get_form_data_for_area(self.tarapaca)
        response = self.client.post(url, data=data)
        self.assertTrue(TakenPosition.objects.filter(person=self.candidate))
        self.assertRedirects(response, reverse('backend_candidate:home'))