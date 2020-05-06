# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (C) 2012-2020 British Crown (Met Office) & Contributors.
# -----------------------------------------------------------------------------

import inspect

import rose.formats
import rose.macro


TRANSFORM_FUNC_NAME = "transform_config"
VALIDATE_FUNC_NAME = "validate_config"


class FormatChecker(rose.macro.MacroBase):

    """Validates against format specifications and conventions."""

    def validate(self, config, meta_config=None):
        """Return a list of errors, if any."""
        self.reports = []
        for attr_name in dir(rose.formats):
            if attr_name.startswith("_"):
                continue
            attr = getattr(rose.formats, attr_name)
            if inspect.ismodule(attr) and hasattr(attr, VALIDATE_FUNC_NAME):
                func = getattr(attr, VALIDATE_FUNC_NAME)
                if inspect.isfunction(func):
                    func(config, meta_config, self.add_report)
        return self.reports


class FormatFixer(rose.macro.MacroBase):

    """Transforms a configuration based on format specifications."""

    def transform(self, config, meta_config=None):
        """Return a config and a list of changes, if any."""
        self.reports = []
        for attr_name in dir(rose.formats):
            if attr_name.startswith("_"):
                continue
            attr = getattr(rose.formats, attr_name)
            if inspect.ismodule(attr) and hasattr(attr, TRANSFORM_FUNC_NAME):
                func = getattr(attr, TRANSFORM_FUNC_NAME)
                if inspect.isfunction(func):
                    config = func(config, meta_config, self.add_report)[0]
        return config, self.reports
