from setuptools import setup, find_packages

setup(
    name = "pyg_annotate",
    version = "0.1",
    author = "LitoNico",
    packages = find_packages(),

    install_requires = ['Pygments >= 1.6'],

    entry_points =

    # A plugin for Pygments that provides a simple markup
    # language for annotating code with Bootstrap popovers.

    """
    [pygments.filters]
    annotation_filter = lib.annotation_filter:AnnotationFilter

    [pygments.formatters]
    annotations_formatter = lib.annotation_formatter:AnnotationHtmlFormatter
    """
)
