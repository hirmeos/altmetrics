from os import path

from django.contrib.auth.models import User
from django.test import Client, TestCase

from importer import forms, models


class ImporterTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        username = 'test_user'
        password = 'test_user_pass'

        self.user = User.objects.create_user(
            username=username,
            password=password
        )
        self.client.login(
            username=username,
            password=password
        )
        self.test_csv = path.join(
            path.dirname(path.realpath(__file__)),
            'import_example.csv'
        )

    def test_adding_csv_saves_csvupload_model(self):
        """ Test that CSVUpload model is created when CSV is added. """

        resp = self.client.get('/new/', follow=True)
        self.assertEqual(resp.status_code, 200)

        csvupload_models = models.CSVUpload.objects.all()
        self.assertEqual(len(csvupload_models), 0)
        form = forms.CSVUploadForm()
        self.assertTrue(form.is_valid())

        # Needs fixing to properly upload file
        with open(self.test_csv) as test_csv:
            self.client.post('/new/', {'file_name': test_csv}, follow=True)

        self.assertEqual(len(csvupload_models), 1)

    def test_saving_csvupload_model_sends_doi_import_task(
            self, register_doi, csv_upload_import_dois
    ):
        """ Test that Celery task to import DOIs is called when
         CSVUpload model is saved.
         """

        pass
        # csv_upload = models.CSVUpload.objects.create(
        #     user=self.user,
        #     file_name='08cee4da11554cca8bc3bdf34855d088-test_import.csv',
        #     link=('https://s3.console.aws.amazon.com/s3/object/metrics-uploads/'
        #           '08cee4da11554cca8bc3bdf34855d088-test_import.csv?region='
        #           'eu-west-1&tab=overview')
        # )
        #
        #
        # # register_doi.assert_called_with(csv_upload.content, csv_upload.pk)
