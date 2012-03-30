# Version constants

PLONE21 = 0
PLONE25 = 0
PLONE30 = 0
PLONE31 = 0
PLONE32 = 0
PLONE33 = 0
PLONE40 = 0
PLONE50 = 0

# Raise exception if no Plone
import Products.CMFPlone

# Check for Plone 2.1 or above
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    PLONE21 = 0
else:
    PLONE21 = 1

# Check for Plone 2.5 or above
try:
    from Products.CMFPlone.migrations import v2_5
except ImportError:
    PLONE25 = 0
else:
    PLONE25 = 1
    PLONE21 = 1

# Check for Plone 3.0 or above
try:
    from Products.CMFPlone.migrations import v3_0
except ImportError:
    PLONE30 = 0
else:
    PLONE30 = 1
    PLONE25 = 1
    PLONE21 = 1

# Check for Plone 3.1 or above
try:
    from Products.CMFPlone.migrations import v3_1
except ImportError:
    PLONE31 = 0
else:
    PLONE31 = 1
    PLONE30 = 1
    PLONE25 = 1
    PLONE21 = 1

# Check for Plone 3.2 or above
try:
    from Products.CMFPlone.migrations import v3_2
except ImportError:
    PLONE32 = 0
else:
    PLONE32 = 1
    PLONE31 = 1
    PLONE30 = 1
    PLONE25 = 1
    PLONE21 = 1

# Check for Plone 3.3 or above
try:
    from Products.CMFPlone.migrations import v3_3
except ImportError:
    PLONE33 = 0
else:
    PLONE33 = 1
    PLONE32 = 1
    PLONE31 = 1
    PLONE30 = 1
    PLONE25 = 1
    PLONE21 = 1

# Check for Plone 4.0 or above
try:
    from Products.CMFPlone.factory import _IMREALLYPLONE4
except ImportError:
    PLONE40 = 0
else:
    PLONE40 = 1
    PLONE33 = 1
    PLONE32 = 1
    PLONE31 = 1
    PLONE30 = 1
    PLONE25 = 1
    PLONE21 = 1

# Check for Plone 4.2 or above
try:
    from plone.app.upgrade import v42
except ImportError:
    PLONE42 = 0
else:
    PLONE42 = 1

# Check for Plone 5.0 or above
try:
    from Products.CMFPlone.factory import _IMREALLYPLONE5
except ImportError:
    PLONE50 = 0
else:
    PLONE50 = 1
    PLONE40 = 1
    PLONE33 = 1
    PLONE32 = 1
    PLONE31 = 1
    PLONE30 = 1
    PLONE25 = 1
    PLONE21 = 1
