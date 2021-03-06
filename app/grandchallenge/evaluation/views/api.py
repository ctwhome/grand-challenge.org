from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.settings import api_settings
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_csv.renderers import PaginatedCSVRenderer
from rest_framework_guardian.filters import ObjectPermissionsFilter

from grandchallenge.evaluation.models import (
    AlgorithmEvaluation,
    Evaluation,
)
from grandchallenge.evaluation.serializers import (
    AlgorithmEvaluationSerializer,
    EvaluationSerializer,
)


class AlgorithmEvaluationViewSet(ReadOnlyModelViewSet):
    queryset = AlgorithmEvaluation.objects.all()
    serializer_class = AlgorithmEvaluationSerializer
    permission_classes = (DjangoObjectPermissions,)
    filter_backends = (
        DjangoFilterBackend,
        ObjectPermissionsFilter,
    )
    filterset_fields = ["submission"]


class EvaluationViewSet(ReadOnlyModelViewSet):
    queryset = (
        Evaluation.objects.all()
        .select_related("submission__phase__challenge", "submission__creator")
        .prefetch_related("outputs__interface")
    )
    serializer_class = EvaluationSerializer
    permission_classes = (DjangoObjectPermissions,)
    filter_backends = (
        DjangoFilterBackend,
        ObjectPermissionsFilter,
    )
    filterset_fields = [
        "submission__phase",
    ]
    renderer_classes = (
        *api_settings.DEFAULT_RENDERER_CLASSES,
        PaginatedCSVRenderer,
    )
