from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('onlinecourse', '0003_choice_rename_question_question_content_submission_and_more')]
    operations = [
        migrations.RenameField(model_name='question', old_name='content', new_name='question_text'),
        migrations.RenameField(model_name='choice', old_name='content', new_name='choice_text'),
        migrations.AlterField(model_name='question', name='grade', field=models.IntegerField(default=1)),
    ]
