AC_INIT(plugins,0.0.1)
AM_INIT_AUTOMAKE(plugins,0.0.1)


AM_PATH_PYTHON()
AC_SUBST(LIBDIR)

AC_PATH_PROG(MSGFMT, msgfmt, AC_MSG_ERROR(Could not find msgfmt))

AC_ARG_WITH(boxtype,
	[  --with-boxtype=NAME box type [[none,dm7025,dm800...]]],
	[BOXTYPE="$withval"],[BOXTYPE="dm800"])

AC_SUBST(BOXTYPE)
AC_DEFINE_UNQUOTED(BOXTYPE,"$BOXTYPE",[box type])

AM_CONDITIONAL([DM8000], [test "$BOXTYPE" = "dm8000"])
AM_CONDITIONAL([DM7025], [test "$BOXTYPE" = "dm7025"])

AC_ARG_WITH(po,
	AS_HELP_STRING([--with-po],[enable updating of po files]),
	[with_po="$withval"],[with_po="no"])
if test "$with_po" = "yes"; then
	AC_PATH_PROG(MSGINIT, msginit)
	AC_PATH_PROG(MSGMERGE, msgmerge)
	AC_PATH_PROG(MSGUNIQ, msguniq)
	AC_PATH_PROG(XGETTEXT, xgettext)
	if test -z "$MSGINIT" -o -z "$MSGMERGE" -o -z "$MSGUNIQ" -o -z "$XGETTEXT"; then
		AC_MSG_ERROR([Could not find required gettext tools])
	fi
fi
AM_CONDITIONAL(UPDATE_PO, test "$with_po" = "yes")

AC_OUTPUT([
Makefile

webadmin/Makefile
webadmin/meta/Makefile
webadmin/src/Makefile
webadmin/src/mobile/Makefile
webadmin/src/web/Makefile
webadmin/src/WebChilds/Makefile
webadmin/src/WebComponents/Makefile
webadmin/src/WebComponents/Sources/Makefile
webadmin/src/web-data/Makefile
webadmin/src/web-data/tpl/Makefile
webadmin/src/web-data/img/Makefile
webadmin/src/WebScreens/Makefile

webbouqueteditor/Makefile
webbouqueteditor/meta/Makefile
webbouqueteditor/src/Makefile
webbouqueteditor/src/web/Makefile
webbouqueteditor/src/web-data/Makefile
webbouqueteditor/src/WebChilds/Makefile
webbouqueteditor/src/WebComponents/Makefile
webbouqueteditor/src/WebComponents/Sources/Makefile
webbouqueteditor/src/WebScreens/Makefile

webinterface/Makefile
webinterface/meta/Makefile
webinterface/src/Makefile
webinterface/src/m/Makefile
webinterface/src/mobile/Makefile
webinterface/src/web/Makefile
webinterface/src/web-data/Makefile
webinterface/src/web-data/fonts/Makefile
webinterface/src/web-data/gfx/Makefile
webinterface/src/web-data/img/Makefile
webinterface/src/web-data/background/Makefile
webinterface/src/web-data/lib/Makefile
webinterface/src/web-data/lib/lang/Makefile
webinterface/src/web-data/lib/datepicker/Makefile
webinterface/src/web-data/lib/datepicker/media/Makefile
webinterface/src/web-data/m/Makefile
webinterface/src/web-data/m/css/Makefile
webinterface/src/web-data/m/css/themes/Makefile
webinterface/src/web-data/m/css/themes/images/Makefile
webinterface/src/web-data/m/script/Makefile
webinterface/src/web-data/tpl/Makefile
webinterface/src/web-data/tpl/default/Makefile
webinterface/src/web-data/tpl/default/streaminterface/Makefile
webinterface/src/WebChilds/Makefile
webinterface/src/WebChilds/External/Makefile
webinterface/src/WebComponents/Makefile
webinterface/src/WebComponents/Converter/Makefile
webinterface/src/WebComponents/Sources/Makefile

F3LEDControl/Makefile
F3LEDControl/src/Makefile
F3LEDControl/meta/Makefile
])
