import random
import factory.fuzzy
import datetime
import pytz
from grandchallenge.annotations.models import (
    AbstractImageAnnotationModel,
    AbstractNamedImageAnnotationModel,
    ETDRSGridAnnotation,
    MeasurementAnnotation,
    BooleanClassificationAnnotation,
    IntegerClassificationAnnotation,
    CoordinateListAnnotation,
    PolygonAnnotationSet,
    SinglePolygonAnnotation,
    LandmarkAnnotationSet,
    SingleLandmarkAnnotation,
)
from tests.cases_tests.factories import ImageFactory
from tests.factories import UserFactory


def create_fake_coordinate_list(size=10):
    c_list = []
    for i in range(size):
        c_list.append([random.uniform(0.0, 1000.0), random.uniform(0.0, 1000.0)])
    return c_list


class DefaultImageAnnotationModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = AbstractImageAnnotationModel
        abstract = True

    image = factory.SubFactory(ImageFactory)
    grader = factory.SubFactory(UserFactory)
    created = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(1950, 1, 1, 0, 0, 0, 0, pytz.UTC)
    )


class ETDRSGridAnnotationFactory(DefaultImageAnnotationModelFactory):
    class Meta:
        model = ETDRSGridAnnotation

    fovea = [random.uniform(0.0, 50.0), random.uniform(0.0, 50.0)]
    optic_disk = [random.uniform(0.0, 50.0), random.uniform(0.0, 50.0)]


class MeasurementAnnotationFactory(DefaultImageAnnotationModelFactory):
    class Meta:
        model = MeasurementAnnotation

    start_voxel = [random.uniform(0.0, 50.0), random.uniform(0.0, 50.0)]
    end_voxel = [random.uniform(0.0, 50.0), random.uniform(0.0, 50.0)]


class DefaultNamedImageAnnotationModelFactory(
    DefaultImageAnnotationModelFactory
):
    class Meta:
        model = AbstractNamedImageAnnotationModel
        abstract = True

    name = factory.fuzzy.FuzzyText()


class BooleanClassificationAnnotationFactory(
    DefaultNamedImageAnnotationModelFactory
):
    class Meta:
        model = BooleanClassificationAnnotation

    value = factory.fuzzy.FuzzyChoice([True, False])


class IntegerClassificationAnnotationFactory(
    DefaultNamedImageAnnotationModelFactory
):
    class Meta:
        model = IntegerClassificationAnnotation

    value = factory.fuzzy.FuzzyInteger(1000)


class CoordinateListAnnotationFactory(DefaultNamedImageAnnotationModelFactory):
    class Meta:
        model = CoordinateListAnnotation

    value = create_fake_coordinate_list()


class PolygonAnnotationSetFactory(DefaultNamedImageAnnotationModelFactory):
    class Meta:
        model = PolygonAnnotationSet


class SinglePolygonAnnotationFactory(factory.DjangoModelFactory):
    class Meta:
        model = SinglePolygonAnnotation

    annotation_set = factory.SubFactory(PolygonAnnotationSetFactory)

    value = create_fake_coordinate_list()


class LandmarkAnnotationSetFactory(factory.DjangoModelFactory):
    class Meta:
        model = LandmarkAnnotationSet

    grader = factory.SubFactory(UserFactory)
    created = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(1950, 1, 1, 0, 0, 0, 0, pytz.UTC)
    )


class SingleLandmarkAnnotationFactory(factory.DjangoModelFactory):
    class Meta:
        model = SingleLandmarkAnnotation

    image = factory.SubFactory(ImageFactory)
    annotation_set = factory.SubFactory(LandmarkAnnotationSetFactory)

    landmarks = create_fake_coordinate_list()


def create_batch_landmarks():
    landmark_annotation_set = LandmarkAnnotationSet()
    landmark_annotations = []
    for i in range(3):
        landmark_annotations.append(
            SingleLandmarkAnnotationFactory(
                registration=landmark_annotation_set
            )
        )

    return landmark_annotation_set, landmark_annotations
