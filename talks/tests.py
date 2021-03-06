from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from .serializers import MeetupSerializer, TalkSerializer
from .models import Meetup, Talk


class MeetupsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_view_name = 'talks:meetups-list'
        self.detail_view_name = 'talks:meetups-detail'
        self.serializer_class = MeetupSerializer

        self.normal_user = User.objects.create(username='test', password='pass')
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@admin.com', password='s3cr3t'
        )

        self.now = timezone.now()
        self.upcoming_meetup = Meetup.objects.create(date=self.now + timedelta(days=3))
        self.past_meetup = Meetup.objects.create(date=self.now - timedelta(days=3))

    def test_meetups_list_with_anonymous_user(self):
        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_meetups_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meetups_list_past_filtering(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(reverse(self.list_view_name), {'only': 'past'})

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['date'], self.past_meetup.date.isoformat().replace('+00:00', 'Z'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meetups_list_upcoming_filtering(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(reverse(self.list_view_name), {'only': 'upcoming'})

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['date'], self.upcoming_meetup.date.isoformat().replace('+00:00', 'Z'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meetups_detail_with_anonymous_user(self):
        response = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.past_meetup.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_meetups_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(
            reverse(self.detail_view_name, kwargs={'pk': self.past_meetup.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['date'], self.past_meetup.date.isoformat().replace('+00:00', 'Z'))

    def test_meetups_create_with_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.post(
            reverse(self.list_view_name),
            data={'date': self.now},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'], 'You do not have permission to perform this action.'
        )

    def test_meetups_create_with_too_long_description(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(
            reverse(self.list_view_name),
            data={'date': self.now, 'description': 'a' * 10001},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['description'], ['Ensure this field has no more than 10000 characters.']
        )

    def test_meetups_create_with_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(
            reverse(self.list_view_name),
            data={'date': self.now},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_meetups_update_with_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.past_meetup.id}),
            data={'date': self.now},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'], 'You do not have permission to perform this action.'
        )

    def test_meetups_update_with_too_long_description(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.upcoming_meetup.id}),
            data={'description': 'a' * 10001},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['description'], ['Ensure this field has no more than 10000 characters.']
        )

    def test_meetups_update_with_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs={'pk': self.past_meetup.id}),
            data={'date': self.now},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['date'], self.now.isoformat().replace('+00:00', 'Z'))

    def test_meetups_delete_with_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.past_meetup.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'], 'You do not have permission to perform this action.'
        )

    def test_meetups_delete_with_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(
            reverse(self.detail_view_name, kwargs={'pk': self.past_meetup.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TalksViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.list_view_name = 'talks:talks-list'
        self.detail_view_name = 'talks:talks-detail'
        self.upvote_view_name = 'talks:talks-upvote'
        self.downvote_view_name = 'talks:talks-downvote'

        self.serializer_class = TalkSerializer

        self.normal_user = User.objects.create(username='test', password='pass')
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@admin.com', password='s3cr3t'
        )

        self.meetup = Meetup.objects.create(date=timezone.now())
        self.first_talk = Talk.objects.create(
            meetup=self.meetup,
            author=self.normal_user,
            topic='first test topic',
            description='first test description'
        )
        self.second_talk = Talk.objects.create(
            meetup=self.meetup,
            author=self.normal_user,
            topic='second test topic',
            description='second test description'
        )

        self.first_detail_kwargs = {'meetups_pk': self.meetup.id, 'pk': self.first_talk.id}
        self.second_detail_kwargs = {'meetups_pk': self.meetup.id, 'pk': self.second_talk.id}
        self.post_data = {'topic': 'test', 'description': 'tests'}

    def test_talks_list_with_anonymous_user(self):
        response = self.client.get(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_talks_list_are_returned_sorted_by_votes(self):
        self.client.force_authenticate(user=self.normal_user)

        self.client.put(reverse(self.upvote_view_name, kwargs=self.second_detail_kwargs))

        response = self.client.get(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['topic'], self.second_talk.topic)
        self.assertEqual(response.data['results'][1]['topic'], self.first_talk.topic)


    def test_talks_list_with_authenticated_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['topic'], self.first_talk.topic)

    def test_talks_detail_with_anonymous_user(self):
        response = self.client.get(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs)
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_talks_detail_with_authenticated_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['topic'], self.first_talk.topic)

    def test_talks_create_with_anonymous_user(self):
        response = self.client.post(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_talks_create_with_too_short_topic(self):
        self.client.force_authenticate(user=self.normal_user)

        self.post_data['topic'] = 'a'
        response = self.client.post(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id}),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['topic'], ['Ensure this field has at least 3 characters.']
        )

    def test_talks_create_with_too_long_topic(self):
        self.client.force_authenticate(user=self.normal_user)

        self.post_data['topic'] *= 500 
        response = self.client.post(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id}),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['topic'], ['Ensure this field has no more than 500 characters.']
        )

    def test_talks_create_with_too_short_description(self):
        self.client.force_authenticate(user=self.normal_user)

        self.post_data['description'] = 'a'
        response = self.client.post(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id}),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['description'], ['Ensure this field has at least 5 characters.']
        )

    def test_talks_create_with_too_long_description(self):
        self.client.force_authenticate(user=self.normal_user)

        self.post_data['description'] *= 10000
        response = self.client.post(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id}),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['description'], ['Ensure this field has no more than 10000 characters.']
        )

    def test_talks_create_with_authenticated_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'meetups_pk': self.meetup.id}),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_talks_update_with_anonymous_user(self):
        response = self.client.put(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_talks_update_with_non_author_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'],
            'You should be the author of this content in order to modify it.'
        )

    def test_talks_update_with_too_short_topic(self):
        self.client.force_authenticate(user=self.normal_user)

        self.post_data['topic'] = 'a'
        response = self.client.put(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['topic'], ['Ensure this field has at least 3 characters.']
        )

    def test_talks_update_with_too_long_topic(self):
        self.client.force_authenticate(user=self.normal_user)

        self.post_data['topic'] *= 500 
        response = self.client.put(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['topic'], ['Ensure this field has no more than 500 characters.']
        )

    def test_talks_update_with_too_short_description(self):
        self.client.force_authenticate(user=self.normal_user)

        self.post_data['description'] = 'a'
        response = self.client.put(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['description'], ['Ensure this field has at least 5 characters.']
        )

    def test_talks_update_with_too_long_description(self):
        self.client.force_authenticate(user=self.normal_user)

        self.post_data['description'] *= 10000
        response = self.client.put(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['description'], ['Ensure this field has no more than 10000 characters.']
        )

    def test_talks_update_with_author_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.put(
            reverse(self.detail_view_name, kwargs=self.first_detail_kwargs),
            data=self.post_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_talks_upvote_with_anonymous_user(self):
        response = self.client.put(reverse(self.upvote_view_name, kwargs=self.first_detail_kwargs))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_talks_upvote_with_authenticated_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.put(reverse(self.upvote_view_name, kwargs=self.first_detail_kwargs))

        self.assertEqual(self.first_talk.votes.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_talks_downvote_with_anonymous_user(self):
        response = self.client.put(reverse(self.downvote_view_name, kwargs=self.first_detail_kwargs))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_talks_downvote_with_authenticated_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.put(reverse(self.upvote_view_name, kwargs=self.first_detail_kwargs))
        self.assertEqual(self.first_talk.votes.count(), 1)

        response = self.client.put(reverse(self.downvote_view_name, kwargs=self.first_detail_kwargs))

        self.assertEqual(self.first_talk.votes.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_talks_destroy_with_anonymous_user(self):
        response = self.client.delete(reverse(self.detail_view_name, kwargs=self.first_detail_kwargs))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_talks_destroy_with_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.delete(reverse(self.detail_view_name, kwargs=self.first_detail_kwargs))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'], 'You do not have permission to perform this action.'
        )

    def test_talks_destroy_with_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(reverse(self.detail_view_name, kwargs=self.first_detail_kwargs))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
