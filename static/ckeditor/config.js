/*
Copyright (c) 2003-2012, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
    config.forcePasteAsPlainText = true;
	config.extraPlugins = 'syntaxhighlight';
	config.toolbar_Full = [
		['Maximize', 'ShowBlocks'],['Iframe'],['Code'],['Source'],
		['Undo','Redo','Replace','RemoveFormat'],
		['Image','Table','SpecialChar'],
		"/",
		['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
		['NumberedList','BulletedList','Blockquote'],
		['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
		['Link','Unlink','Anchor'],
		['Styles','FontSize'],
		['TextColor','BGColor'],
		
	 ];
     CKEDITOR.config.font_names='';
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
};
