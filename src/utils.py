from typing import Union, Tuple, Type

from rest_framework import views, serializers
from rest_framework.serializers import ListSerializer


class ExportFileMixin:
    """
    Mixin which allows the override of the filename being
    passed back to the user when the file is downloaded.
    """

    excel_filename = "protrend_data.xlsx"
    csv_filename = "protrend_data.csv"
    fasta_filename = "protrend_data.fasta"

    def get_excel_filename(self):
        """
        Returns a custom filename for the spreadsheet.
        """
        return self.excel_filename

    def get_csv_filename(self):
        """
        Returns a custom filename for the csv.
        """
        return self.csv_filename

    def get_fasta_filename(self):
        """
        Returns a custom filename for the fasta.
        """
        return self.fasta_filename

    def finalize_response(self: Union['ExportFileMixin', views.APIView], request, response, *args, **kwargs):
        """
        Return the response with the proper content disposition and the customized
        filename instead of the browser default (or lack thereof).
        """
        response = super(ExportFileMixin, self).finalize_response(request, response, *args, **kwargs)

        if response.accepted_renderer.format == 'xlsx':
            filename = self.get_excel_filename()
            response["content-disposition"] = f"attachment; filename={filename}"

        elif response.accepted_renderer.format == 'csv':
            filename = self.get_csv_filename()
            response["content-disposition"] = f"attachment; filename={filename}"

        elif response.accepted_renderer.format == 'fasta':
            filename = self.get_fasta_filename()
            response["content-disposition"] = f"attachment; filename={filename}"

        return response


def get_header(serializer_cls: Type[serializers.Serializer], nested_fields: Tuple = None) -> Tuple:
    serializer = serializer_cls()

    if not nested_fields:
        nested_fields = ()

    header = []
    for key, value in serializer.fields.items():

        if key in nested_fields:

            if hasattr(value, 'child'):
                value = value.child

            for sub_key in value.fields.keys():
                nested_key = f'{key}.{sub_key}'
                header.append(nested_key)

        else:
            header.append(key)

    return tuple(header)
