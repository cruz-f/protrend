from typing import Union, Tuple, Type

from rest_framework import serializers, generics


class ExportFileMixin:
    """
    Mixin which allows the override of the filename being
    passed back to the user when the file is downloaded.
    """

    json_filename = "protrend_data.json"
    excel_filename = "protrend_data.xlsx"
    csv_filename = "protrend_data.csv"
    nucleotide_fasta_filename = "protrend_data.fna"
    amino_acid_fasta_filename = "protrend_data.faa"
    nucleotide_gnb_filename = "protrend_data.gbff"
    amino_acid_gnb_filename = "protrend_data.gpff"
    xlsx_ignore_headers = []

    def finalize_response(self: Union['ExportFileMixin', generics.GenericAPIView], request, response, *args, **kwargs):
        """
        Return the response with the proper content disposition and the customized
        filename instead of the browser default (or lack thereof).
        """
        response = super(ExportFileMixin, self).finalize_response(request, response, *args, **kwargs)

        if response.accepted_renderer.format == 'json':
            filename = self.json_filename
            response["content-disposition"] = f"attachment; filename={filename}"

        elif response.accepted_renderer.format == 'xlsx':
            filename = self.excel_filename
            response["content-disposition"] = f"attachment; filename={filename}"

        elif response.accepted_renderer.format == 'csv':
            filename = self.csv_filename
            response["content-disposition"] = f"attachment; filename={filename}"

        elif response.accepted_renderer.format == 'fna':
            filename = self.nucleotide_fasta_filename
            response["content-disposition"] = f"attachment; filename={filename}"

        elif response.accepted_renderer.format == 'faa':
            filename = self.amino_acid_fasta_filename
            response["content-disposition"] = f"attachment; filename={filename}"

        elif response.accepted_renderer.format == 'gbff':
            filename = self.nucleotide_gnb_filename
            response["content-disposition"] = f"attachment; filename={filename}"

        elif response.accepted_renderer.format == 'gpff':
            filename = self.amino_acid_gnb_filename
            response["content-disposition"] = f"attachment; filename={filename}"

        return response

    def get_renderer_context(self: Union['ExportFileMixin', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        header, ignore_headers = get_header(serializer_cls=serializer_cls)
        self.xlsx_ignore_headers = ignore_headers

        context['header'] = header
        return context


def get_header(serializer_cls: Type[serializers.Serializer], nested_fields: Tuple = None) -> Tuple:
    serializer = serializer_cls()

    if not nested_fields:
        nested_fields = ()

    header = []
    ignore_headers = []
    for key, value in serializer.fields.items():

        if value.write_only:
            ignore_headers.append(key)
            continue

        if key in nested_fields:

            if hasattr(value, 'child'):
                value = value.child

            for sub_key in value.fields.keys():
                nested_key = f'{key}.{sub_key}'
                header.append(nested_key)

        else:
            header.append(key)

    return tuple(header), ignore_headers
