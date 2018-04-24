from django.db import models
from django.template.defaultfilters import slugify
from accounts.models import Company

class Industry(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Post, self).save(*args, **kwargs)


JOB_TYPES = (
        ('fulltime', 'Full-Time'),
        ('parttime', 'Part-Time')
    )

MIN_QUALIFICATIONS = (
    ('ssce', 'SSCE'),
    ('bsc', 'BSc'),
    ('msc', 'MSc'),
    ('phd', 'PhD')
)

YEARS_OF_EXP = (
    ('entry', 'Entry Level'),
    ('1-2', '1-2 years'),
    ('3-5', '3-5 years'),
    ('6-10', '6-10 years'),
    ('above 10', 'Above 10 years')
)

class Job(models.Model):
    title               = models.CharField(max_length=60)
    slug                = models.SlugField()
    industry            = models.ForeignKey(Industry, on_delete=models.CASCADE)
    company             = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_type            = models.CharField(max_length=10, choices=JOB_TYPES)
    min_qualification   = models.CharField('Minimum Qualification', max_length=10, choices=MIN_QUALIFICATIONS, null=True, blank=True)
    years_of_exp        = models.CharField('Years of Experience', max_length=20, choices=YEARS_OF_EXP, null=True, blank=True)
    salary              = models.PositiveIntegerField(blank=True, null=True)
    description         = models.TextField()
    # expires_on = models.DateTimeField()
    posted_on           = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)