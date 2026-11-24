#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCII Tool & Character Reference
================================
A comprehensive utility for ASCII characters, decoding, encoding,
and full reference table.

Usage:
    python3 ascii.py [options] [values ...]

Examples:
    # Show printable characters table (codes 32-126)
    python3 ascii.py --printable
    python3 ascii.py -p --category digits
    python3 ascii.py -p --category symbols
    python3 ascii.py -p --compact
    python3 ascii.py -p --grid

    # Search characters by symbol, code, entity, or name
    python3 ascii.py --search "quote"
    python3 ascii.py -s "!"
    python3 ascii.py -s "amp"

    # Inspect a character by decimal code or symbol
    python3 ascii.py --info 33
    python3 ascii.py --info "!"

    # Encode a string to various ASCII formats (dec, hex, bin, oct, html, sql)
    python3 ascii.py --encode "Hello World"
    python3 ascii.py --encode "admin' OR 1=1--" --to sql

    # Decode decimal values
    python3 ascii.py 104 101 108 108 111

    # Decode hex values
    python3 ascii.py --hex 68 65 6c 6c 6f

    # Decode SQL injection string
    python3 ascii.py --sql "CHAR(104, 101, 108, 108, 111)"

    # Show standard (0-127), control (0-31, 127), or extended (128-255) tables
    python3 ascii.py --table
    python3 ascii.py --control-table
    python3 ascii.py --extended-table
"""

import sys
import argparse
import re
import html as html_lib
import urllib.parse
from typing import List, Tuple, Dict, Any, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

try:
    import rich_argparse
    HelpFormatter = rich_argparse.RichHelpFormatter
except ImportError:
    HelpFormatter = argparse.RawDescriptionHelpFormatter

console = Console()

# ============================================================================
# DATA TABLES
# ============================================================================

PRINTABLE_RAW = [(32, '20', ' ', '&#32;', '&nbsp;', '', 'Space', 'Whitespace'), (33, '21', '!', '&#33;', '&excl;', '', 'Exclamation mark', 'Punctuation / Symbol'), (34, '22', '"', '&#34;', '&quot;', '&QUOT;', 'Double quotes (or speech marks)', 'Punctuation / Symbol'), (35, '23', '#', '&#35;', '&num;', '', 'Number sign', 'Punctuation / Symbol'), (36, '24', '$', '&#36;', '&dollar;', '', 'Dollar', 'Punctuation / Symbol'), (37, '25', '%', '&#37;', '&percnt;', '', 'Per cent sign', 'Punctuation / Symbol'), (38, '26', '&', '&#38;', '&amp;', '&AMP;', 'Ampersand', 'Punctuation / Symbol'), (39, '27', "'", '&#39;', '&apos;', '', 'Single quote', 'Punctuation / Symbol'), (40, '28', '(', '&#40;', '&lparen;', '&lpar;', 'Open parenthesis (or open bracket)', 'Punctuation / Symbol'), (41, '29', ')', '&#41;', '&rparen;', '&rpar;', 'Close parenthesis (or close bracket)', 'Punctuation / Symbol'), (42, '2A', '*', '&#42;', '&ast;', '&midast;', 'Asterisk', 'Punctuation / Symbol'), (43, '2B', '+', '&#43;', '&plus;', '', 'Plus', 'Punctuation / Symbol'), (44, '2C', ',', '&#44;', '&comma;', '', 'Comma', 'Punctuation / Symbol'), (45, '2D', '-', '&#45;', '', '', 'Hyphen-minus', 'Punctuation / Symbol'), (46, '2E', '.', '&#46;', '&period;', '', 'Period, dot or full stop', 'Punctuation / Symbol'), (47, '2F', '/', '&#47;', '&sol;', '', 'Slash or divide', 'Punctuation / Symbol'), (48, '30', '0', '&#48;', '', '', 'Zero', 'Digit'), (49, '31', '1', '&#49;', '', '', 'One', 'Digit'), (50, '32', '2', '&#50;', '', '', 'Two', 'Digit'), (51, '33', '3', '&#51;', '', '', 'Three', 'Digit'), (52, '34', '4', '&#52;', '', '', 'Four', 'Digit'), (53, '35', '5', '&#53;', '', '', 'Five', 'Digit'), (54, '36', '6', '&#54;', '', '', 'Six', 'Digit'), (55, '37', '7', '&#55;', '', '', 'Seven', 'Digit'), (56, '38', '8', '&#56;', '', '', 'Eight', 'Digit'), (57, '39', '9', '&#57;', '', '', 'Nine', 'Digit'), (58, '3A', ':', '&#58;', '&colon;', '', 'Colon', 'Punctuation / Symbol'), (59, '3B', ';', '&#59;', '&semi;', '', 'Semicolon', 'Punctuation / Symbol'), (60, '3C', '<', '&#60;', '&lt;', '&LT;', 'Less than (or open angled bracket)', 'Punctuation / Symbol'), (61, '3D', '=', '&#61;', '&equals;', '', 'Equals', 'Punctuation / Symbol'), (62, '3E', '>', '&#62;', '&gt;', '&GT;', 'Greater than (or close angled bracket)', 'Punctuation / Symbol'), (63, '3F', '?', '&#63;', '&quest;', '', 'Question mark', 'Punctuation / Symbol'), (64, '40', '@', '&#64;', '&commat;', '', 'At sign', 'Punctuation / Symbol'), (65, '41', 'A', '&#65;', '', '', 'Uppercase A', 'Uppercase Letter'), (66, '42', 'B', '&#66;', '', '', 'Uppercase B', 'Uppercase Letter'), (67, '43', 'C', '&#67;', '', '', 'Uppercase C', 'Uppercase Letter'), (68, '44', 'D', '&#68;', '', '', 'Uppercase D', 'Uppercase Letter'), (69, '45', 'E', '&#69;', '', '', 'Uppercase E', 'Uppercase Letter'), (70, '46', 'F', '&#70;', '', '', 'Uppercase F', 'Uppercase Letter'), (71, '47', 'G', '&#71;', '', '', 'Uppercase G', 'Uppercase Letter'), (72, '48', 'H', '&#72;', '', '', 'Uppercase H', 'Uppercase Letter'), (73, '49', 'I', '&#73;', '', '', 'Uppercase I', 'Uppercase Letter'), (74, '4A', 'J', '&#74;', '', '', 'Uppercase J', 'Uppercase Letter'), (75, '4B', 'K', '&#75;', '', '', 'Uppercase K', 'Uppercase Letter'), (76, '4C', 'L', '&#76;', '', '', 'Uppercase L', 'Uppercase Letter'), (77, '4D', 'M', '&#77;', '', '', 'Uppercase M', 'Uppercase Letter'), (78, '4E', 'N', '&#78;', '', '', 'Uppercase N', 'Uppercase Letter'), (79, '4F', 'O', '&#79;', '', '', 'Uppercase O', 'Uppercase Letter'), (80, '50', 'P', '&#80;', '', '', 'Uppercase P', 'Uppercase Letter'), (81, '51', 'Q', '&#81;', '', '', 'Uppercase Q', 'Uppercase Letter'), (82, '52', 'R', '&#82;', '', '', 'Uppercase R', 'Uppercase Letter'), (83, '53', 'S', '&#83;', '', '', 'Uppercase S', 'Uppercase Letter'), (84, '54', 'T', '&#84;', '', '', 'Uppercase T', 'Uppercase Letter'), (85, '55', 'U', '&#85;', '', '', 'Uppercase U', 'Uppercase Letter'), (86, '56', 'V', '&#86;', '', '', 'Uppercase V', 'Uppercase Letter'), (87, '57', 'W', '&#87;', '', '', 'Uppercase W', 'Uppercase Letter'), (88, '58', 'X', '&#88;', '', '', 'Uppercase X', 'Uppercase Letter'), (89, '59', 'Y', '&#89;', '', '', 'Uppercase Y', 'Uppercase Letter'), (90, '5A', 'Z', '&#90;', '', '', 'Uppercase Z', 'Uppercase Letter'), (91, '5B', '[', '&#91;', '&lsqb;', '&lbrack;', 'Opening bracket', 'Punctuation / Symbol'), (92, '5C', '\\', '&#92;', '&bsol;', '', 'Backslash', 'Punctuation / Symbol'), (93, '5D', ']', '&#93;', '&rsqb;', '&rbrack;', 'Closing bracket', 'Punctuation / Symbol'), (94, '5E', '^', '&#94;', '&Hat;', '', 'Caret - circumflex', 'Punctuation / Symbol'), (95, '5F', '_', '&#95;', '&lowbar;', '', 'Underscore', 'Punctuation / Symbol'), (96, '60', '`', '&#96;', '&grave;', '&DiacriticalGrave;', 'Grave accent', 'Punctuation / Symbol'), (97, '61', 'a', '&#97;', '', '', 'Lowercase a', 'Lowercase Letter'), (98, '62', 'b', '&#98;', '', '', 'Lowercase b', 'Lowercase Letter'), (99, '63', 'c', '&#99;', '', '', 'Lowercase c', 'Lowercase Letter'), (100, '64', 'd', '&#100;', '', '', 'Lowercase d', 'Lowercase Letter'), (101, '65', 'e', '&#101;', '', '', 'Lowercase e', 'Lowercase Letter'), (102, '66', 'f', '&#102;', '', '', 'Lowercase f', 'Lowercase Letter'), (103, '67', 'g', '&#103;', '', '', 'Lowercase g', 'Lowercase Letter'), (104, '68', 'h', '&#104;', '', '', 'Lowercase h', 'Lowercase Letter'), (105, '69', 'i', '&#105;', '', '', 'Lowercase i', 'Lowercase Letter'), (106, '6A', 'j', '&#106;', '', '', 'Lowercase j', 'Lowercase Letter'), (107, '6B', 'k', '&#107;', '', '', 'Lowercase k', 'Lowercase Letter'), (108, '6C', 'l', '&#108;', '', '', 'Lowercase l', 'Lowercase Letter'), (109, '6D', 'm', '&#109;', '', '', 'Lowercase m', 'Lowercase Letter'), (110, '6E', 'n', '&#110;', '', '', 'Lowercase n', 'Lowercase Letter'), (111, '6F', 'o', '&#111;', '', '', 'Lowercase o', 'Lowercase Letter'), (112, '70', 'p', '&#112;', '', '', 'Lowercase p', 'Lowercase Letter'), (113, '71', 'q', '&#113;', '', '', 'Lowercase q', 'Lowercase Letter'), (114, '72', 'r', '&#114;', '', '', 'Lowercase r', 'Lowercase Letter'), (115, '73', 's', '&#115;', '', '', 'Lowercase s', 'Lowercase Letter'), (116, '74', 't', '&#116;', '', '', 'Lowercase t', 'Lowercase Letter'), (117, '75', 'u', '&#117;', '', '', 'Lowercase u', 'Lowercase Letter'), (118, '76', 'v', '&#118;', '', '', 'Lowercase v', 'Lowercase Letter'), (119, '77', 'w', '&#119;', '', '', 'Lowercase w', 'Lowercase Letter'), (120, '78', 'x', '&#120;', '', '', 'Lowercase x', 'Lowercase Letter'), (121, '79', 'y', '&#121;', '', '', 'Lowercase y', 'Lowercase Letter'), (122, '7A', 'z', '&#122;', '', '', 'Lowercase z', 'Lowercase Letter'), (123, '7B', '{', '&#123;', '&lcub;', '&lbrace;', 'Opening brace', 'Punctuation / Symbol'), (124, '7C', '|', '&#124;', '&verbar;', '&vert;', 'Vertical bar', 'Punctuation / Symbol'), (125, '7D', '}', '&#125;', '&rcub;', '&rbrace;', 'Closing brace', 'Punctuation / Symbol'), (126, '7E', '~', '&#126;', '&tilde;', '', 'Equivalency sign - tilde', 'Punctuation / Symbol')]

CONTROL_RAW = [(0, '00', '␀', '&#00;', '', '', 'Null character', 'Control Character'), (1, '01', '␁', '&#01;', '', '', 'Start of Heading', 'Control Character'), (2, '02', '␂', '&#02;', '', '', 'Start of Text', 'Control Character'), (3, '03', '␃', '&#03;', '', '', 'End of Text', 'Control Character'), (4, '04', '␄', '&#04;', '', '', 'End of Transmission', 'Control Character'), (5, '05', '␅', '&#05;', '', '', 'Enquiry', 'Control Character'), (6, '06', '␆', '&#06;', '', '', 'Acknowledge', 'Control Character'), (7, '07', '␇', '&#07;', '', '', 'Bell, Alert', 'Control Character'), (8, '08', '␈', '&#08;', '', '', 'Backspace', 'Control Character'), (9, '09', '␉', '&#09;', '&Tab;', '', 'Horizontal Tab', 'Control Character'), (10, '0A', '␊', '&#10;', '&NewLine;', '', 'Line Feed', 'Control Character'), (11, '0B', '␋', '&#11;', '', '', 'Vertical Tabulation', 'Control Character'), (12, '0C', '␌', '&#12;', '', '', 'Form Feed', 'Control Character'), (13, '0D', '␍', '&#13;', '', '', 'Carriage Return', 'Control Character'), (14, '0E', '␎', '&#14;', '', '', 'Shift Out', 'Control Character'), (15, '0F', '␏', '&#15;', '', '', 'Shift In', 'Control Character'), (16, '10', '␐', '&#16;', '', '', 'Data Link Escape', 'Control Character'), (17, '11', '␑', '&#17;', '', '', 'Device Control One (XON)', 'Control Character'), (18, '12', '␒', '&#18;', '', '', 'Device Control Two', 'Control Character'), (19, '13', '␓', '&#19;', '', '', 'Device Control Three (XOFF)', 'Control Character'), (20, '14', '␔', '&#20;', '', '', 'Device Control Four', 'Control Character'), (21, '15', '␕', '&#21;', '', '', 'Negative Acknowledge', 'Control Character'), (22, '16', '␖', '&#22;', '', '', 'Synchronous Idle', 'Control Character'), (23, '17', '␗', '&#23;', '', '', 'End of Transmission Block', 'Control Character'), (24, '18', '␘', '&#24;', '', '', 'Cancel', 'Control Character'), (25, '19', '␙', '&#25;', '', '', 'End of medium', 'Control Character'), (26, '1A', '␚', '&#26;', '', '', 'Substitute', 'Control Character'), (27, '1B', '␛', '&#27;', '', '', 'Escape', 'Control Character'), (28, '1C', '␜', '&#28;', '', '', 'File Separator', 'Control Character'), (29, '1D', '␝', '&#29;', '', '', 'Group Separator', 'Control Character'), (30, '1E', '␞', '&#30;', '', '', 'Record Separator', 'Control Character'), (31, '1F', '␟', '&#31;', '', '', 'Unit Separator', 'Control Character'), (127, '7F', '␡', '&#127;', '', '', 'Delete', 'Control Character')]


# Extended ASCII (128-255) - ISO-8859-1 / Windows-1252
EXTENDED_RAW = [
    (128, '80', '€', '&#128;', '&euro;', '', 'Euro Sign', 'Extended ASCII'),
    (129, '81', '', '&#129;', '', '', 'Unused', 'Extended ASCII'),
    (130, '82', '‚', '&#130;', '&sbquo;', '', 'Single Low-9 Quotation Mark', 'Extended ASCII'),
    (131, '83', 'ƒ', '&#131;', '&fnof;', '', 'Latin Small Letter F with Hook', 'Extended ASCII'),
    (132, '84', '„', '&#132;', '&bdquo;', '', 'Double Low-9 Quotation Mark', 'Extended ASCII'),
    (133, '85', '…', '&#133;', '&hellip;', '', 'Horizontal Ellipsis', 'Extended ASCII'),
    (134, '86', '†', '&#134;', '&dagger;', '', 'Dagger', 'Extended ASCII'),
    (135, '87', '‡', '&#135;', '&Dagger;', '', 'Double Dagger', 'Extended ASCII'),
    (136, '88', 'ˆ', '&#136;', '&circ;', '', 'Modifier Letter Circumflex Accent', 'Extended ASCII'),
    (137, '89', '‰', '&#137;', '&permil;', '', 'Per Mille Sign', 'Extended ASCII'),
    (138, '8A', 'Š', '&#138;', '&Scaron;', '', 'Latin Capital Letter S with Caron', 'Extended ASCII'),
    (139, '8B', '‹', '&#139;', '&lsaquo;', '', 'Single Left-Pointing Angle Quotation Mark', 'Extended ASCII'),
    (140, '8C', 'Œ', '&#140;', '&OElig;', '', 'Latin Capital Ligature OE', 'Extended ASCII'),
    (141, '8D', '', '&#141;', '', '', 'Unused', 'Extended ASCII'),
    (142, '8E', 'Ž', '&#142;', '&Zcaron;', '', 'Latin Capital Letter Z with Caron', 'Extended ASCII'),
    (143, '8F', '', '&#143;', '', '', 'Unused', 'Extended ASCII'),
    (144, '90', '', '&#144;', '', '', 'Unused', 'Extended ASCII'),
    (145, '91', '‘', '&#145;', '&lsquo;', '', 'Left Single Quotation Mark', 'Extended ASCII'),
    (146, '92', '’', '&#146;', '&rsquo;', '', 'Right Single Quotation Mark', 'Extended ASCII'),
    (147, '93', '“', '&#147;', '&ldquo;', '', 'Left Double Quotation Mark', 'Extended ASCII'),
    (148, '94', '”', '&#148;', '&rdquo;', '', 'Right Double Quotation Mark', 'Extended ASCII'),
    (149, '95', '•', '&#149;', '&bull;', '', 'Bullet', 'Extended ASCII'),
    (150, '96', '–', '&#150;', '&ndash;', '', 'En Dash', 'Extended ASCII'),
    (151, '97', '—', '&#151;', '&mdash;', '', 'Em Dash', 'Extended ASCII'),
    (152, '98', '˜', '&#152;', '&tilde;', '', 'Small Tilde', 'Extended ASCII'),
    (153, '99', '™', '&#153;', '&trade;', '', 'Trade Mark Sign', 'Extended ASCII'),
    (154, '9A', 'š', '&#154;', '&scaron;', '', 'Latin Small Letter S with Caron', 'Extended ASCII'),
    (155, '9B', '›', '&#155;', '&rsaquo;', '', 'Single Right-Pointing Angle Quotation Mark', 'Extended ASCII'),
    (156, '9C', 'œ', '&#156;', '&oelig;', '', 'Latin Small Ligature OE', 'Extended ASCII'),
    (157, '9D', '', '&#157;', '', '', 'Unused', 'Extended ASCII'),
    (158, '9E', 'ž', '&#158;', '&zcaron;', '', 'Latin Small Letter Z with Caron', 'Extended ASCII'),
    (159, '9F', 'Ÿ', '&#159;', '&Yuml;', '', 'Latin Capital Letter Y with Diaeresis', 'Extended ASCII'),
    (160, 'A0', ' ', '&#160;', '&nbsp;', '', 'No-Break Space', 'Extended ASCII'),
    (161, 'A1', '¡', '&#161;', '&iexcl;', '', 'Inverted Exclamation Mark', 'Extended ASCII'),
    (162, 'A2', '¢', '&#162;', '&cent;', '', 'Cent Sign', 'Extended ASCII'),
    (163, 'A3', '£', '&#163;', '&pound;', '', 'Pound Sign', 'Extended ASCII'),
    (164, 'A4', '¤', '&#164;', '&curren;', '', 'Currency Sign', 'Extended ASCII'),
    (165, 'A5', '¥', '&#165;', '&yen;', '', 'Yen Sign', 'Extended ASCII'),
    (166, 'A6', '¦', '&#166;', '&brvbar;', '', 'Broken Bar', 'Extended ASCII'),
    (167, 'A7', '§', '&#167;', '&sect;', '', 'Section Sign', 'Extended ASCII'),
    (168, 'A8', '¨', '&#168;', '&uml;', '', 'Diaeresis', 'Extended ASCII'),
    (169, 'A9', '©', '&#169;', '&copy;', '', 'Copyright Sign', 'Extended ASCII'),
    (170, 'AA', 'ª', '&#170;', '&ordf;', '', 'Feminine Ordinal Indicator', 'Extended ASCII'),
    (171, 'AB', '«', '&#171;', '&laquo;', '', 'Left-Pointing Double Angle Quotation Mark', 'Extended ASCII'),
    (172, 'AC', '¬', '&#172;', '&not;', '', 'Not Sign', 'Extended ASCII'),
    (173, 'AD', '­', '&#173;', '&shy;', '', 'Soft Hyphen', 'Extended ASCII'),
    (174, 'AE', '®', '&#174;', '&reg;', '', 'Registered Sign', 'Extended ASCII'),
    (175, 'AF', '¯', '&#175;', '&macr;', '', 'Macron', 'Extended ASCII'),
    (176, 'B0', '°', '&#176;', '&deg;', '', 'Degree Sign', 'Extended ASCII'),
    (177, 'B1', '±', '&#177;', '&plusmn;', '', 'Plus-Minus Sign', 'Extended ASCII'),
    (178, 'B2', '²', '&#178;', '&sup2;', '', 'Superscript Two', 'Extended ASCII'),
    (179, 'B3', '³', '&#179;', '&sup3;', '', 'Superscript Three', 'Extended ASCII'),
    (180, 'B4', '´', '&#180;', '&acute;', '', 'Acute Accent', 'Extended ASCII'),
    (181, 'B5', 'µ', '&#181;', '&micro;', '', 'Micro Sign', 'Extended ASCII'),
    (182, 'B6', '¶', '&#182;', '&para;', '', 'Pilcrow Sign', 'Extended ASCII'),
    (183, 'B7', '·', '&#183;', '&middot;', '', 'Middle Dot', 'Extended ASCII'),
    (184, 'B8', '¸', '&#184;', '&cedil;', '', 'Cedilla', 'Extended ASCII'),
    (185, 'B9', '¹', '&#185;', '&sup1;', '', 'Superscript One', 'Extended ASCII'),
    (186, 'BA', 'º', '&#186;', '&ordm;', '', 'Masculine Ordinal Indicator', 'Extended ASCII'),
    (187, 'BB', '»', '&#187;', '&raquo;', '', 'Right-Pointing Double Angle Quotation Mark', 'Extended ASCII'),
    (188, 'BC', '¼', '&#188;', '&frac14;', '', 'Vulgar Fraction One Quarter', 'Extended ASCII'),
    (189, 'BD', '½', '&#189;', '&frac12;', '', 'Vulgar Fraction One Half', 'Extended ASCII'),
    (190, 'BE', '¾', '&#190;', '&frac34;', '', 'Vulgar Fraction Three Quarters', 'Extended ASCII'),
    (191, 'BF', '¿', '&#191;', '&iquest;', '', 'Inverted Question Mark', 'Extended ASCII'),
    (192, 'C0', 'À', '&#192;', '&Agrave;', '', 'Latin Capital Letter A with Grave', 'Extended ASCII'),
    (193, 'C1', 'Á', '&#193;', '&Aacute;', '', 'Latin Capital Letter A with Acute', 'Extended ASCII'),
    (194, 'C2', 'Â', '&#194;', '&Acirc;', '', 'Latin Capital Letter A with Circumflex', 'Extended ASCII'),
    (195, 'C3', 'Ã', '&#195;', '&Atilde;', '', 'Latin Capital Letter A with Tilde', 'Extended ASCII'),
    (196, 'C4', 'Ä', '&#196;', '&Auml;', '', 'Latin Capital Letter A with Diaeresis', 'Extended ASCII'),
    (197, 'C5', 'Å', '&#197;', '&Aring;', '', 'Latin Capital Letter A with Ring Above', 'Extended ASCII'),
    (198, 'C6', 'Æ', '&#198;', '&AElig;', '', 'Latin Capital Letter AE', 'Extended ASCII'),
    (199, 'C7', 'Ç', '&#199;', '&Ccedil;', '', 'Latin Capital Letter C with Cedilla', 'Extended ASCII'),
    (200, 'C8', 'È', '&#200;', '&Egrave;', '', 'Latin Capital Letter E with Grave', 'Extended ASCII'),
    (201, 'C9', 'É', '&#201;', '&Eacute;', '', 'Latin Capital Letter E with Acute', 'Extended ASCII'),
    (202, 'CA', 'Ê', '&#202;', '&Ecirc;', '', 'Latin Capital Letter E with Circumflex', 'Extended ASCII'),
    (203, 'CB', 'Ë', '&#203;', '&Euml;', '', 'Latin Capital Letter E with Diaeresis', 'Extended ASCII'),
    (204, 'CC', 'Ì', '&#204;', '&Igrave;', '', 'Latin Capital Letter I with Grave', 'Extended ASCII'),
    (205, 'CD', 'Í', '&#205;', '&Iacute;', '', 'Latin Capital Letter I with Acute', 'Extended ASCII'),
    (206, 'CE', 'Î', '&#206;', '&Icirc;', '', 'Latin Capital Letter I with Circumflex', 'Extended ASCII'),
    (207, 'CF', 'Ï', '&#207;', '&Iuml;', '', 'Latin Capital Letter I with Diaeresis', 'Extended ASCII'),
    (208, 'D0', 'Ð', '&#208;', '&ETH;', '', 'Latin Capital Letter Eth', 'Extended ASCII'),
    (209, 'D1', 'Ñ', '&#209;', '&Ntilde;', '', 'Latin Capital Letter N with Tilde', 'Extended ASCII'),
    (210, 'D2', 'Ò', '&#210;', '&Ograve;', '', 'Latin Capital Letter O with Grave', 'Extended ASCII'),
    (211, 'D3', 'Ó', '&#211;', '&Oacute;', '', 'Latin Capital Letter O with Acute', 'Extended ASCII'),
    (212, 'D4', 'Ô', '&#212;', '&Ocirc;', '', 'Latin Capital Letter O with Circumflex', 'Extended ASCII'),
    (213, 'D5', 'Õ', '&#213;', '&Otilde;', '', 'Latin Capital Letter O with Tilde', 'Extended ASCII'),
    (214, 'D6', 'Ö', '&#214;', '&Ouml;', '', 'Latin Capital Letter O with Diaeresis', 'Extended ASCII'),
    (215, 'D7', '×', '&#215;', '&times;', '', 'Multiplication Sign', 'Extended ASCII'),
    (216, 'D8', 'Ø', '&#216;', '&Oslash;', '', 'Latin Capital Letter O with Stroke', 'Extended ASCII'),
    (217, 'D9', 'Ù', '&#217;', '&Ugrave;', '', 'Latin Capital Letter U with Grave', 'Extended ASCII'),
    (218, 'DA', 'Ú', '&#218;', '&Uacute;', '', 'Latin Capital Letter U with Acute', 'Extended ASCII'),
    (219, 'DB', 'Û', '&#219;', '&Ucirc;', '', 'Latin Capital Letter U with Circumflex', 'Extended ASCII'),
    (220, 'DC', 'Ü', '&#220;', '&Uuml;', '', 'Latin Capital Letter U with Diaeresis', 'Extended ASCII'),
    (221, 'DD', 'Ý', '&#221;', '&Yacute;', '', 'Latin Capital Letter Y with Acute', 'Extended ASCII'),
    (222, 'DE', 'Þ', '&#222;', '&THORN;', '', 'Latin Capital Letter Thorn', 'Extended ASCII'),
    (223, 'DF', 'ß', '&#223;', '&szlig;', '', 'Latin Small Letter Sharp S', 'Extended ASCII'),
    (224, 'E0', 'à', '&#224;', '&agrave;', '', 'Latin Small Letter A with Grave', 'Extended ASCII'),
    (225, 'E1', 'á', '&#225;', '&aacute;', '', 'Latin Small Letter A with Acute', 'Extended ASCII'),
    (226, 'E2', 'â', '&#226;', '&acirc;', '', 'Latin Small Letter A with Circumflex', 'Extended ASCII'),
    (227, 'E3', 'ã', '&#227;', '&atilde;', '', 'Latin Small Letter A with Tilde', 'Extended ASCII'),
    (228, 'E4', 'ä', '&#228;', '&auml;', '', 'Latin Small Letter A with Diaeresis', 'Extended ASCII'),
    (229, 'E5', 'å', '&#229;', '&aring;', '', 'Latin Small Letter A with Ring Above', 'Extended ASCII'),
    (230, 'E6', 'æ', '&#230;', '&aelig;', '', 'Latin Small Letter AE', 'Extended ASCII'),
    (231, 'E7', 'ç', '&#231;', '&ccedil;', '', 'Latin Small Letter C with Cedilla', 'Extended ASCII'),
    (232, 'E8', 'è', '&#232;', '&egrave;', '', 'Latin Small Letter E with Grave', 'Extended ASCII'),
    (233, 'E9', 'é', '&#233;', '&eacute;', '', 'Latin Small Letter E with Acute', 'Extended ASCII'),
    (234, 'EA', 'ê', '&#234;', '&ecirc;', '', 'Latin Small Letter E with Circumflex', 'Extended ASCII'),
    (235, 'EB', 'ë', '&#235;', '&euml;', '', 'Latin Small Letter E with Diaeresis', 'Extended ASCII'),
    (236, 'EC', 'ì', '&#236;', '&igrave;', '', 'Latin Small Letter I with Grave', 'Extended ASCII'),
    (237, 'ED', 'í', '&#237;', '&iacute;', '', 'Latin Small Letter I with Acute', 'Extended ASCII'),
    (238, 'EE', 'î', '&#238;', '&icirc;', '', 'Latin Small Letter I with Circumflex', 'Extended ASCII'),
    (239, 'EF', 'ï', '&#239;', '&iuml;', '', 'Latin Small Letter I with Diaeresis', 'Extended ASCII'),
    (240, 'F0', 'ð', '&#240;', '&eth;', '', 'Latin Small Letter Eth', 'Extended ASCII'),
    (241, 'F1', 'ñ', '&#241;', '&ntilde;', '', 'Latin Small Letter N with Tilde', 'Extended ASCII'),
    (242, 'F2', 'ò', '&#242;', '&ograve;', '', 'Latin Small Letter O with Grave', 'Extended ASCII'),
    (243, 'F3', 'ó', '&#243;', '&oacute;', '', 'Latin Small Letter O with Acute', 'Extended ASCII'),
    (244, 'F4', 'ô', '&#244;', '&ocirc;', '', 'Latin Small Letter O with Circumflex', 'Extended ASCII'),
    (245, 'F5', 'õ', '&#245;', '&otilde;', '', 'Latin Small Letter O with Tilde', 'Extended ASCII'),
    (246, 'F6', 'ö', '&#246;', '&ouml;', '', 'Latin Small Letter O with Diaeresis', 'Extended ASCII'),
    (247, 'F7', '÷', '&#247;', '&divide;', '', 'Division Sign', 'Extended ASCII'),
    (248, 'F8', 'ø', '&#248;', '&oslash;', '', 'Latin Small Letter O with Stroke', 'Extended ASCII'),
    (249, 'F9', 'ù', '&#249;', '&ugrave;', '', 'Latin Small Letter U with Grave', 'Extended ASCII'),
    (250, 'FA', 'ú', '&#250;', '&uacute;', '', 'Latin Small Letter U with Acute', 'Extended ASCII'),
    (251, 'FB', 'û', '&#251;', '&ucirc;', '', 'Latin Small Letter U with Circumflex', 'Extended ASCII'),
    (252, 'FC', 'ü', '&#252;', '&uuml;', '', 'Latin Small Letter U with Diaeresis', 'Extended ASCII'),
    (253, 'FD', 'ý', '&#253;', '&yacute;', '', 'Latin Small Letter Y with Acute', 'Extended ASCII'),
    (254, 'FE', 'þ', '&#254;', '&thorn;', '', 'Latin Small Letter Thorn', 'Extended ASCII'),
    (255, 'FF', 'ÿ', '&#255;', '&yuml;', '', 'Latin Small Letter Y with Diaeresis', 'Extended ASCII'),
]

# Lookup dictionary for all code points
ASCII_DATABASE = {}

for item in CONTROL_RAW + PRINTABLE_RAW + EXTENDED_RAW:
    code, hx, sym, html_num, html_name, html_name2, name, cat = item
    ASCII_DATABASE[code] = {
        'code': code,
        'hex': hx,
        'oct': oct(code)[2:].zfill(3),
        'bin': format(code, '08b'),
        'symbol': sym,
        'html_number': html_num,
        'html_name': html_name,
        'html_name2': html_name2,
        'name': name,
        'category': cat,
    }


# ============================================================================
# MODERN STYLING & FORMATTING HELPERS
# ============================================================================

CATEGORY_COLORS = {
    'Digit': 'bold cyan',
    'Uppercase Letter': 'bold green',
    'Lowercase Letter': 'bold chartreuse3',
    'Punctuation / Symbol': 'bold yellow',
    'Whitespace': 'dim white',
    'Control Character': 'bold bright_red',
    'Extended ASCII': 'bold magenta',
}


def format_category(cat: str) -> Text:
    color = CATEGORY_COLORS.get(cat, 'white')
    return Text(cat, style=color)


def format_symbol(code: int, sym: str) -> Text:
    if code == 32:
        return Text("[SP]", style="bold bright_cyan")
    if code < 32 or code == 127:
        return Text(sym if sym else "·", style="bold bright_red")
    if 32 < code <= 126:
        return Text(sym, style="bold bright_yellow")
    if 128 <= code <= 255:
        return Text(sym if sym else "·", style="bold magenta")
    return Text(sym if sym else "·", style="white")


def print_banner():
    banner_text = Text()
    banner_text.append("⚡ ASCII Tool & Character Reference\n", style="bold bright_cyan")
    banner_text.append("Standard (0-127)  •  Control (0-31, 127)  •  Extended (128-255)  •  Encoder & Decoder", style="dim")
    console.print()
    console.print(Panel(banner_text, box=box.ROUNDED, border_style="cyan", padding=(0, 2)))


def print_character_card(code: int, index: Optional[int] = None):
    entry = ASCII_DATABASE.get(code)
    if not entry:
        console.print(f"\n[bold red][-] Character code #{code} not found in ASCII database (valid range 0-255).[/bold red]\n")
        return

    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="bold cyan", justify="right")
    grid.add_column(style="white")
    grid.add_column(style="bold cyan", justify="right")
    grid.add_column(style="white")

    sym_disp = format_symbol(code, entry['symbol'])
    cat_disp = format_category(entry['category'])
    html_name = entry['html_name'] if entry['html_name'] else "(none)"
    html_name2 = entry['html_name2'] if entry['html_name2'] else "(none)"

    grid.add_row("Decimal", str(entry['code']), "HTML Number", entry['html_number'])
    grid.add_row("Hexadecimal", f"0x{entry['hex']} ({entry['hex']})", "HTML Entity", html_name)
    grid.add_row("Binary", entry['bin'], "HTML Entity 2", html_name2)
    grid.add_row("Octal", f"0o{entry['oct']}", "Category", cat_disp)
    grid.add_row("Symbol", sym_disp, "Official Name", entry['name'])

    idx_prefix = f"[{index}] " if index is not None else ""
    sym_label = repr(entry['symbol']) if entry['symbol'] else 'None'
    title = f"[bold bright_cyan]⚡ Character Detail: [bold bright_yellow]{sym_label}[/bold bright_yellow] ({idx_prefix}Code #{code})[/bold bright_cyan]"
    panel = Panel(
        grid,
        title=title,
        box=box.ROUNDED,
        border_style="bright_blue",
        padding=(1, 3)
    )
    console.print(panel)


class DecodedCharDetail:
    def __init__(self, index: int, dec: int, char: str, entry: Dict[str, Any]):
        self.index = index
        self.dec = dec
        self.char = char
        self.entry = entry

    def __str__(self) -> str:
        display = self.char if len(self.char) == 1 else repr(self.char)
        html_disp = self.entry.get('html_name') or self.entry.get('html_number', '')
        return (
            f"  [{self.index:3d}]  dec={self.dec:3d}  hex=0x{self.entry.get('hex', '')}  "
            f"bin={self.entry.get('bin', '')}  oct={self.entry.get('oct', ''):>4}  "
            f"html={html_disp:<11}  char={display:<4}  {self.entry.get('name', '')}"
        )


# ============================================================================
# ASCII TOOL ENGINE
# ============================================================================

class ASCIITool:
    """ASCII tool with full support for printable, control, and extended characters."""

    def __init__(self, show_nonprintable=False, show_control=False,
                 show_extended=True, full_detail=False, sql_mode=False):
        self.show_nonprintable = show_nonprintable
        self.show_control = show_control
        self.show_extended = show_extended
        self.full_detail = full_detail
        self.sql_mode = sql_mode

    # ---- Display & Table Methods ---------------------------------------

    def print_printable_table(self, category=None):
        """Display ASCII Printable Characters table (32-126)."""
        filtered = []
        for code in range(32, 127):
            entry = ASCII_DATABASE[code]
            if category:
                c = category.lower()
                cat = entry['category'].lower()
                if c == 'digits' and entry['category'] == 'Digit':
                    filtered.append(entry)
                elif c in ('uppercase', 'upper') and entry['category'] == 'Uppercase Letter':
                    filtered.append(entry)
                elif c in ('lowercase', 'lower') and entry['category'] == 'Lowercase Letter':
                    filtered.append(entry)
                elif c in ('letters', 'alpha') and 'Letter' in entry['category']:
                    filtered.append(entry)
                elif c in ('symbols', 'punct', 'punctuation') and 'Symbol' in entry['category']:
                    filtered.append(entry)
                elif c in ('space', 'whitespace') and entry['category'] == 'Whitespace':
                    filtered.append(entry)
                elif c in cat:
                    filtered.append(entry)
            else:
                filtered.append(entry)

        title = "⚡ ASCII Printable Characters (Codes 32 to 126)"
        if category:
            title += f"  •  Filter: {category.upper()}"

        table = Table(
            title=title,
            title_style="bold bright_cyan",
            caption=f"Showing {len(filtered)} character(s)  •  Printable Range: 32 to 126",
            caption_style="dim",
            box=box.ROUNDED,
            border_style="bright_cyan",
            header_style="bold bright_cyan",
        )
        table.add_column("Dec", justify="right", style="bold cyan")
        table.add_column("HEX", justify="center", style="magenta")
        table.add_column("Oct", justify="right", style="blue")
        table.add_column("Binary", justify="center", style="dim green")
        table.add_column("Sym", justify="center")
        table.add_column("HTML Num", style="dim")
        table.add_column("HTML Entity", style="yellow")
        table.add_column("Category")
        table.add_column("Official Name", style="white")

        for e in filtered:
            sym_disp = format_symbol(e['code'], e['symbol'])
            html_ent = e['html_name']
            if e['html_name2']:
                html_ent = f"{e['html_name']} ({e['html_name2']})"
            table.add_row(
                str(e['code']),
                e['hex'],
                e['oct'],
                e['bin'],
                sym_disp,
                e['html_number'],
                html_ent,
                format_category(e['category']),
                e['name']
            )

        console.print()
        console.print(table)
        console.print()

    def print_compact_view(self, category=None):
        """Compact table view matching modern CLI layout."""
        table = Table(
            title="⚡ ASCII Printable Characters • Compact View",
            title_style="bold bright_cyan",
            box=box.ROUNDED,
            border_style="bright_blue",
            header_style="bold bright_cyan",
        )
        table.add_column("Dec", justify="right", style="bold cyan")
        table.add_column("HEX", justify="center", style="magenta")
        table.add_column("Sym", justify="center")
        table.add_column("HTML Entity", style="yellow")
        table.add_column("Category")
        table.add_column("Official Name", style="white")

        for code in range(32, 127):
            e = ASCII_DATABASE[code]
            if category:
                c = category.lower()
                if c == 'digits' and e['category'] != 'Digit':
                    continue
                if c in ('uppercase', 'upper') and e['category'] != 'Uppercase Letter':
                    continue
                if c in ('lowercase', 'lower') and e['category'] != 'Lowercase Letter':
                    continue
                if c in ('symbols', 'punctuation') and 'Symbol' not in e['category']:
                    continue
                if c in ('letters', 'alpha') and 'Letter' not in e['category']:
                    continue
                if c in ('space', 'whitespace') and e['category'] != 'Whitespace':
                    continue

            sym_disp = format_symbol(code, e['symbol'])
            html_ent = e['html_name']
            if e['html_name2']:
                html_ent = f"{e['html_name']} ({e['html_name2']})"
            table.add_row(
                str(e['code']),
                e['hex'],
                sym_disp,
                html_ent,
                format_category(e['category']),
                e['name']
            )

        console.print()
        console.print(table)
        console.print()

    def print_grid_view(self, category=None):
        """Modern responsive grid view."""
        title = "⚡ ASCII Printable Characters • Grid View"
        if category:
            title += f" ({category.upper()})"

        table = Table(
            title=title,
            title_style="bold bright_cyan",
            caption="Printable Codes 32 to 126",
            caption_style="dim",
            box=box.ROUNDED,
            border_style="bright_blue",
            show_header=False,
            padding=(0, 1)
        )
        for _ in range(8):
            table.add_column(justify="center")

        items = []
        for code in range(32, 127):
            e = ASCII_DATABASE[code]
            if category:
                c = category.lower()
                if c == 'digits' and e['category'] != 'Digit':
                    continue
                if c in ('uppercase', 'upper') and e['category'] != 'Uppercase Letter':
                    continue
                if c in ('lowercase', 'lower') and e['category'] != 'Lowercase Letter':
                    continue
                if c in ('symbols', 'punctuation') and 'Symbol' not in e['category']:
                    continue
                if c in ('letters', 'alpha') and 'Letter' not in e['category']:
                    continue
                if c in ('space', 'whitespace') and e['category'] != 'Whitespace':
                    continue

            sym_str = "[SP]" if code == 32 else e['symbol']
            sym_style = "bold bright_yellow"
            if e['category'] == 'Digit':
                sym_style = "bold bright_cyan"
            elif 'Upper' in e['category']:
                sym_style = "bold bright_green"
            elif 'Lower' in e['category']:
                sym_style = "bold chartreuse3"

            cell = Text()
            cell.append(f"{code:3d} ", style="dim cyan")
            cell.append(f"{sym_str:^4}", style=sym_style)
            items.append(cell)

        for i in range(0, len(items), 8):
            row = items[i:i+8]
            while len(row) < 8:
                row.append(Text(""))
            table.add_row(*row)

        console.print()
        console.print(table)
        console.print()

    def print_standard_table(self):
        """Print full standard ASCII table (0-127)."""
        table = Table(
            title="⚡ Standard ASCII Table (Codes 0 to 127)",
            title_style="bold bright_cyan",
            caption="Total: 128 characters (0-31 Control, 32-126 Printable, 127 Delete)",
            caption_style="dim",
            box=box.ROUNDED,
            border_style="cyan",
            header_style="bold bright_cyan",
        )
        table.add_column("Dec", justify="right", style="bold cyan")
        table.add_column("HEX", justify="center", style="magenta")
        table.add_column("Oct", justify="right", style="blue")
        table.add_column("Binary", justify="center", style="dim green")
        table.add_column("Sym", justify="center")
        table.add_column("HTML", style="yellow")
        table.add_column("Category")
        table.add_column("Official Name", style="white")

        for code in range(0, 128):
            e = ASCII_DATABASE[code]
            sym_disp = format_symbol(code, e['symbol'])
            html_disp = e['html_name'] if e['html_name'] else e['html_number']
            table.add_row(
                str(e['code']),
                e['hex'],
                e['oct'],
                e['bin'],
                sym_disp,
                html_disp,
                format_category(e['category']),
                e['name']
            )

        console.print()
        console.print(table)
        console.print()

    def print_control_table(self):
        """Print ASCII Control Characters table (0-31, 127)."""
        table = Table(
            title="⚡ ASCII Control Characters (Codes 0-31, 127)",
            title_style="bold bright_red",
            caption="Total: 33 Control Characters",
            caption_style="dim",
            box=box.ROUNDED,
            border_style="bright_red",
            header_style="bold bright_red",
        )
        table.add_column("Dec", justify="right", style="bold cyan")
        table.add_column("HEX", justify="center", style="magenta")
        table.add_column("Oct", justify="right", style="blue")
        table.add_column("Binary", justify="center", style="dim green")
        table.add_column("Sym", justify="center")
        table.add_column("HTML Num", style="dim")
        table.add_column("HTML Name", style="yellow")
        table.add_column("Official Name / Description", style="white")

        for code in list(range(32)) + [127]:
            e = ASCII_DATABASE[code]
            sym_disp = format_symbol(code, e['symbol'])
            table.add_row(
                str(e['code']),
                e['hex'],
                e['oct'],
                e['bin'],
                sym_disp,
                e['html_number'],
                e['html_name'],
                e['name']
            )

        console.print()
        console.print(table)
        console.print()

    def print_extended_table(self):
        """Print Extended ASCII table (128-255)."""
        table = Table(
            title="⚡ Extended ASCII Table (Codes 128-255) • ISO-8859-1 / Windows-1252",
            title_style="bold magenta",
            caption="Total: 128 Extended Characters",
            caption_style="dim",
            box=box.ROUNDED,
            border_style="magenta",
            header_style="bold magenta",
        )
        table.add_column("Dec", justify="right", style="bold cyan")
        table.add_column("HEX", justify="center", style="magenta")
        table.add_column("Oct", justify="right", style="blue")
        table.add_column("Binary", justify="center", style="dim green")
        table.add_column("Sym", justify="center")
        table.add_column("HTML", style="yellow")
        table.add_column("Official Name", style="white")

        for code in range(128, 256):
            e = ASCII_DATABASE[code]
            sym_disp = format_symbol(code, e['symbol'])
            html_disp = e['html_name'] if e['html_name'] else e['html_number']
            table.add_row(
                str(e['code']),
                e['hex'],
                e['oct'],
                e['bin'],
                sym_disp,
                html_disp,
                e['name']
            )

        console.print()
        console.print(table)
        console.print()

    def print_character_info(self, query):
        """Display comprehensive modern detail card for a character code or symbol."""
        code = None
        if isinstance(query, int):
            code = query
        elif isinstance(query, str):
            if query.isdigit():
                code = int(query)
            elif query.startswith(('0x', '0X')):
                try:
                    code = int(query, 16)
                except ValueError:
                    pass
            elif len(query) == 1:
                code = ord(query)

        if code is None or code not in ASCII_DATABASE:
            console.print(f"\n[bold red][-] Character '{query}' not found in ASCII database (valid range 0-255).[/bold red]\n")
            return

        print_character_card(code)

    def search(self, query):
        """Search character database by symbol, code, entity, or description."""
        q = query.strip()
        matches = []
        numeric_code = None
        if q.isdigit():
            numeric_code = int(q)
        elif q.lower().startswith(('0x', '0b', '0o')):
            try:
                numeric_code = int(q, 0)
            except ValueError:
                pass

        for code, entry in ASCII_DATABASE.items():
            hit = False
            if numeric_code is not None and code == numeric_code:
                hit = True
            elif entry['symbol'] and entry['symbol'] == q:
                hit = True
            elif q.lower() in entry['name'].lower():
                hit = True
            elif q.lower() in entry['category'].lower():
                hit = True
            elif entry['html_name'] and q.lower() in entry['html_name'].lower():
                hit = True
            elif entry['html_name2'] and q.lower() in entry['html_name2'].lower():
                hit = True
            elif entry['html_number'] and q in entry['html_number']:
                hit = True
            elif entry['hex'].lower() == q.lower().replace('0x', ''):
                hit = True

            if hit:
                matches.append(entry)

        if not matches:
            console.print()
            console.print(Panel(
                f"[bold yellow]No ASCII characters found matching:[/] [bold cyan]{query}[/]",
                box=box.ROUNDED,
                border_style="yellow",
                padding=(0, 2)
            ))
            console.print()
            return

        table = Table(
            title=f"⚡ ASCII Search Results for '{query}'",
            title_style="bold bright_cyan",
            caption=f"Found {len(matches)} matching character(s)",
            caption_style="dim",
            box=box.ROUNDED,
            border_style="bright_blue",
            header_style="bold bright_cyan",
        )
        table.add_column("Dec", justify="right", style="bold cyan")
        table.add_column("HEX", justify="center", style="magenta")
        table.add_column("Oct", justify="right", style="blue")
        table.add_column("Binary", justify="center", style="dim green")
        table.add_column("Sym", justify="center")
        table.add_column("HTML", style="yellow")
        table.add_column("Category")
        table.add_column("Official Name", style="white")

        for e in matches:
            sym_disp = format_symbol(e['code'], e['symbol'])
            html_disp = e['html_name'] if e['html_name'] else e['html_number']
            table.add_row(
                str(e['code']),
                e['hex'],
                e['oct'],
                e['bin'],
                sym_disp,
                html_disp,
                format_category(e['category']),
                e['name']
            )

        console.print()
        console.print(table)
        console.print()

    # ---- Encoding Methods ----------------------------------------------

    def encode_text(self, text, to_format=None):
        """Encode a string into various ASCII formats."""
        codes = [ord(ch) for ch in text]
        
        dec_str = " ".join(str(c) for c in codes)
        hex_str = " ".join(f"{c:02x}" for c in codes)
        hex_prefix_str = " ".join(f"0x{c:02x}" for c in codes)
        hex_continuous = "".join(f"{c:02x}" for c in codes)
        bin_str = " ".join(f"{c:08b}" for c in codes)
        oct_str = " ".join(oct(c)[2:].zfill(3) for c in codes)
        
        html_num_str = "".join(f"&#{c};" for c in codes)
        html_entities_list = []
        for c in codes:
            entry = ASCII_DATABASE.get(c)
            if entry and entry['html_name']:
                html_entities_list.append(entry['html_name'])
            else:
                html_entities_list.append(chr(c) if 32 <= c <= 126 else f"&#{c};")
        html_ent_str = "".join(html_entities_list)

        sql_char = f"CHAR({','.join(str(c) for c in codes)})"
        sql_chr_concat = "||".join(f"CHR({c})" for c in codes)
        url_encoded = urllib.parse.quote(text)
        url_full = "".join(f"%{c:02X}" for c in codes)

        if to_format:
            fmt = to_format.lower()
            mapping = {
                'dec': dec_str, 'decimal': dec_str,
                'hex': hex_str, 'hexadecimal': hex_str,
                'hex-prefix': hex_prefix_str, '0x': hex_prefix_str,
                'hex-continuous': hex_continuous, 'hex-cont': hex_continuous,
                'bin': bin_str, 'binary': bin_str,
                'oct': oct_str, 'octal': oct_str,
                'html': html_num_str, 'html-num': html_num_str,
                'html-ent': html_ent_str, 'entity': html_ent_str,
                'sql': sql_char, 'sql-char': sql_char,
                'sql-concat': sql_chr_concat,
                'url': url_encoded, 'url-encoded': url_encoded,
                'url-hex': url_full,
            }
            print(mapping.get(fmt, dec_str))
            return

        table = Table(
            title=f"⚡ ASCII Encoding Breakdown for {repr(text)}",
            title_style="bold bright_cyan",
            caption=f"Length: {len(text)} character(s)  •  {len(codes)} byte(s)",
            caption_style="dim",
            box=box.ROUNDED,
            border_style="bright_blue",
            header_style="bold bright_cyan",
        )
        table.add_column("Format", style="bold cyan", width=22)
        table.add_column("Encoded Value", style="bright_white")
        table.add_column("Type / Notes", style="dim")

        table.add_row("Decimal", dec_str, "Space-separated decimal integers")
        table.add_row("Hex (spaced)", hex_str, "Space-separated hex pairs")
        table.add_row("Hex (prefixed)", hex_prefix_str, "0x-prefixed values")
        table.add_row("Hex (continuous)", f"0x{hex_continuous}", "Continuous byte string")
        table.add_row("Binary", bin_str, "8-bit binary representation")
        table.add_row("Octal", oct_str, "Base-8 octal representation")
        table.add_row("HTML Number", html_num_str, "Decimal character entities")
        table.add_row("HTML Entity", html_ent_str, "Named character entities")
        table.add_row("SQL (MySQL/MSSQL)", sql_char, "SQL CHAR() function call")
        table.add_row("SQL (Oracle/Postgres)", sql_chr_concat, "SQL CHR() concatenation")
        table.add_row("URL Encoded", url_encoded, "Percent-encoded query string")
        table.add_row("URL Full Hex", url_full, "Full percent-hex encoded bytes")

        console.print()
        console.print(table)
        console.print()

    # ---- Decoding Methods ----------------------------------------------

    def decode_auto(self, values):
        """Auto-detect format (decimal, hex, bin, oct, sql, html) and decode."""
        full_text = " ".join(values)
        
        # Check SQL CHAR pattern e.g. CHAR(104, 101, 108, 108, 111)
        sql_match = re.search(r'CHAR\s*\(\s*([\d\s,]+)\s*\)', full_text, re.IGNORECASE)
        if sql_match:
            nums = [int(n.strip()) for n in sql_match.group(1).split(',') if n.strip().isdigit()]
            return self._decode_values(nums)

        # Check CHR(...) pattern
        chr_matches = re.findall(r'CHR\s*\(\s*(\d+)\s*\)', full_text, re.IGNORECASE)
        if chr_matches:
            nums = [int(n) for n in chr_matches]
            return self._decode_values(nums)

        # Check continuous hex string: e.g. 0x68656c6c6f or 68656c6c6f with len > 4 and even length
        cleaned = full_text.strip()
        if cleaned.startswith(('0x', '0X')):
            hex_body = cleaned[2:]
            if re.match(r'^[0-9a-fA-F]+$', hex_body) and len(hex_body) % 2 == 0 and len(hex_body) > 2:
                nums = [int(hex_body[i:i+2], 16) for i in range(0, len(hex_body), 2)]
                return self._decode_values(nums)

        # Check HTML entities e.g. &#104;&#101; or &quot;
        if '&' in full_text and ';' in full_text:
            decoded_html = html_lib.unescape(full_text)
            nums = [ord(c) for c in decoded_html]
            return self._decode_values(nums)

        decimals = []
        for v in values:
            v = v.strip().rstrip(',')
            if not v:
                continue
            if v.startswith(('0x', '0X')):
                decimals.append(int(v, 16))
            elif v.startswith(('0b', '0B')):
                decimals.append(int(v, 2))
            elif v.startswith(('0o', '0O')):
                decimals.append(int(v, 8))
            elif re.match(r'^[01]+$', v) and len(v) >= 7:
                decimals.append(int(v, 2))
            elif re.match(r'^[0-9a-fA-F]+$', v) and len(v) == 2 and not v.isdigit():
                decimals.append(int(v, 16))
            else:
                decimals.append(int(v))

        return self._decode_values(decimals)

    def decode_hex(self, values):
        """Decode hexadecimal values."""
        if len(values) == 1 and len(values[0]) > 2 and len(values[0]) % 2 == 0:
            val = values[0].replace('0x', '').replace('0X', '')
            if re.match(r'^[0-9a-fA-F]+$', val):
                return self._decode_values([int(val[i:i+2], 16) for i in range(0, len(val), 2)])
        return self._decode_values([int(v, 16) for v in values])

    def decode_binary(self, values):
        """Decode binary values."""
        return self._decode_values([int(v, 2) for v in values])

    def decode_octal(self, values):
        """Decode octal values."""
        return self._decode_values([int(v, 8) for v in values])

    def decode_from_file(self, filepath, fmt='auto'):
        """Decode ASCII values from file."""
        with open(filepath, 'r') as f:
            content = f.read().strip()
        if not content:
            return '', []
        values = [v for v in re.split(r'\s+', content) if v]
        dispatch = {
            'decimal': lambda vs: self._decode_values([int(x) for x in vs]),
            'hex': self.decode_hex,
            'binary': self.decode_binary,
            'octal': self.decode_octal,
            'auto': self.decode_auto,
        }
        return dispatch.get(fmt, self.decode_auto)(values)

    def _format_char(self, dec):
        """Format single character for decoded-string output."""
        entry = ASCII_DATABASE.get(dec)
        if entry:
            if dec < 32 or dec == 127:
                if self.show_control:
                    abbr = entry['name'].split()[0]
                    return f"<{abbr}>"
                if self.show_nonprintable:
                    return f"\\x{dec:02x}"
                return "."
            if 32 <= dec <= 126:
                return chr(dec)
            if 128 <= dec <= 255:
                if self.show_extended:
                    return entry['symbol'] if entry['symbol'] else f"\\x{dec:02x}"
                if self.show_nonprintable:
                    return f"\\x{dec:02x}"
                return "."
        if self.show_nonprintable:
            return f"\\x{dec:02x}"
        return "."

    def _decode_values(self, decimals):
        """Core decoder: convert decimal values to string + detail lines."""
        result = []
        details = []
        for i, dec in enumerate(decimals):
            char = self._format_char(dec)
            result.append(char)
            entry = ASCII_DATABASE.get(dec, {
                'code': dec,
                'hex': f"{dec:02x}",
                'oct': oct(dec)[2:],
                'bin': format(dec, '08b'),
                'symbol': '',
                'html_number': f"&#{dec};",
                'html_name': '',
                'html_name2': '',
                'name': 'Unknown',
                'category': 'Out of Range',
            })
            details.append(DecodedCharDetail(i, dec, char, entry))
        return "".join(result), details


# ============================================================================
# RESULTS & CLI INTERFACE
# ============================================================================

def print_results(decoded, details, verbose=False, full=False):
    console.print()
    panel = Panel(
        Text(decoded, style="bold bright_green"),
        title="[bold bright_cyan]✨ Decoded String[/bold bright_cyan]",
        subtitle=f"[dim]{len(decoded)} character(s)  •  Raw: {repr(decoded)}[/dim]",
        box=box.ROUNDED,
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)

    if verbose and not full:
        table = Table(
            title="⚡ Character Breakdown",
            title_style="bold bright_cyan",
            box=box.ROUNDED,
            border_style="bright_blue",
            header_style="bold bright_cyan",
        )
        table.add_column("#", justify="right", style="dim")
        table.add_column("Dec", justify="right", style="bold cyan")
        table.add_column("HEX", justify="center", style="magenta")
        table.add_column("Oct", justify="right", style="blue")
        table.add_column("Binary", justify="center", style="dim green")
        table.add_column("Char", justify="center")
        table.add_column("HTML", style="yellow")
        table.add_column("Category")
        table.add_column("Official Name", style="white")

        for d in details:
            e = d.entry
            sym = format_symbol(d.dec, d.char)
            cat = format_category(e.get('category', 'Unknown'))
            html_disp = e.get('html_name') or e.get('html_number', '')
            table.add_row(
                str(d.index),
                str(d.dec),
                f"0x{e.get('hex', '')}",
                e.get('oct', ''),
                e.get('bin', ''),
                sym,
                html_disp,
                cat,
                e.get('name', 'Unknown')
            )
        console.print()
        console.print(table)

    if full:
        console.print()
        for d in details:
            print_character_card(d.dec, index=d.index)

    console.print()


def main():
    parser = argparse.ArgumentParser(
        description="ASCII Tool - Modern Reference & Converter",
        formatter_class=HelpFormatter,
    )

    # Values to decode or inspect
    parser.add_argument('values', nargs='*', default=[],
                        help='ASCII values to decode (decimal, hex, bin, oct, or SQL CHAR)')
    parser.add_argument('-f', '--file',
                        help='Read values from file (whitespace-separated)')

    # Table options
    table_group = parser.add_argument_group('Table Displays')
    table_group.add_argument('-p', '--printable', '--printable-table', action='store_true',
                             help='Print ASCII Printable Characters table (32-126)')
    table_group.add_argument('-t', '--table', action='store_true',
                             help='Print standard ASCII table (0-127)')
    table_group.add_argument('-C', '--control-table', action='store_true',
                             help='Print ASCII control characters table (0-31, 127)')
    table_group.add_argument('-e', '--extended-table', action='store_true',
                             help='Print extended ASCII table (128-255)')
    table_group.add_argument('--compact', action='store_true',
                             help='Use compact view for printable characters')
    table_group.add_argument('--grid', action='store_true',
                             help='Use grid view for printable characters')
    table_group.add_argument('--category',
                             help='Filter printable table by category (digits, uppercase, lowercase, letters, symbols, space)')

    # Search and Info
    lookup_group = parser.add_argument_group('Search & Character Lookup')
    lookup_group.add_argument('-s', '--search',
                             help='Search characters by symbol, code, HTML entity, or description')
    lookup_group.add_argument('-i', '--info', '--char',
                             help='Inspect single character detail by decimal code or symbol')

    # Encoding
    encode_group = parser.add_argument_group('Encoding')
    encode_group.add_argument('-E', '--encode',
                             help='Encode text string to various ASCII representations')
    encode_group.add_argument('--to',
                             help='Specific target format for --encode (dec, hex, bin, oct, html, sql, url)')

    # Decoding Format Flags
    fmt_group = parser.add_argument_group('Decoding Formats')
    fmt_group.add_argument('-d', '--decimal', action='store_true',
                           help='Input values are decimal (default)')
    fmt_group.add_argument('-x', '--hex', action='store_true',
                           help='Input values are hexadecimal')
    fmt_group.add_argument('-b', '--binary', action='store_true',
                           help='Input values are binary')
    fmt_group.add_argument('-o', '--octal', action='store_true',
                           help='Input values are octal')
    fmt_group.add_argument('-a', '--auto', action='store_true',
                           help='Auto-detect input format (hex, binary, SQL CHAR, HTML entities)')
    fmt_group.add_argument('--sql', '--sql-mode', dest='sql_mode', action='store_true',
                           help='Decode SQL injection expressions (e.g. CHAR(104,101,108) or 0x68656c)')

    # Output Options
    out_group = parser.add_argument_group('Output Options')
    out_group.add_argument('-v', '--verbose', action='store_true',
                           help='Show per-character breakdown table')
    out_group.add_argument('-F', '--full', action='store_true',
                           help='Full detail card per character')
    out_group.add_argument('-n', '--nonprintable', action='store_true',
                           help='Show non-printable chars as \\xHH')
    out_group.add_argument('-c', '--control', action='store_true',
                           help='Show control chars as <NAME>')
    out_group.add_argument('--no-extended', action='store_true',
                           help='Do not render extended ASCII (128-255)')
    out_group.add_argument('-O', '--output',
                           help='Write decoded output to file')
    out_group.add_argument('--no-banner', action='store_true',
                           help='Suppress banner')

    args = parser.parse_args()

    tool = ASCIITool(
        show_nonprintable=args.nonprintable,
        show_control=args.control,
        show_extended=not args.no_extended,
        full_detail=args.full,
        sql_mode=args.sql_mode,
    )

    # 1. Printable characters table
    if args.printable or args.compact or args.grid or args.category:
        if not args.no_banner:
            print_banner()
        if args.compact:
            tool.print_compact_view(category=args.category)
        elif args.grid:
            tool.print_grid_view(category=args.category)
        else:
            tool.print_printable_table(category=args.category)
        return

    # 2. Other tables
    if args.table:
        if not args.no_banner:
            print_banner()
        tool.print_standard_table()
        return

    if args.control_table:
        if not args.no_banner:
            print_banner()
        tool.print_control_table()
        return

    if args.extended_table:
        if not args.no_banner:
            print_banner()
        tool.print_extended_table()
        return

    # 3. Search query
    if args.search:
        if not args.no_banner:
            print_banner()
        tool.search(args.search)
        return

    # 4. Single character inspector
    if args.info:
        if not args.no_banner:
            print_banner()
        tool.print_character_info(args.info)
        return

    # 5. Text encoding
    if args.encode:
        if not args.no_banner and not args.to:
            print_banner()
        tool.encode_text(args.encode, to_format=args.to)
        return

    # 6. Decode values
    if not args.values and not args.file:
        if not args.no_banner:
            print_banner()
        tool.print_printable_table()
        return

    if not args.no_banner:
        print_banner()

    fmt = ('decimal' if args.decimal else
           'hex' if args.hex else
           'binary' if args.binary else
           'octal' if args.octal else
           'auto')

    try:
        if args.file:
            decoded, details = tool.decode_from_file(args.file, fmt)
        else:
            values = args.values
            if len(values) == 1 and ('CHAR(' in values[0].upper() or 'CHR(' in values[0].upper()):
                decoded, details = tool.decode_auto(values)
            elif fmt == 'decimal':
                decoded, details = tool._decode_values([int(v.rstrip(',')) for v in values])
            elif fmt == 'hex':
                decoded, details = tool.decode_hex(values)
            elif fmt == 'binary':
                decoded, details = tool.decode_binary(values)
            elif fmt == 'octal':
                decoded, details = tool.decode_octal(values)
            else:
                decoded, details = tool.decode_auto(values)

        print_results(decoded, details, args.verbose, args.full)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(decoded)
            console.print(f"[bold green][✓][/] Decoded string written to: [cyan]{args.output}[/]\n")

    except ValueError as e:
        console.print(f"[bold red][-] Error:[/] Invalid value format — {e}")
        sys.exit(1)
    except FileNotFoundError:
        console.print(f"[bold red][-] Error:[/] File not found — {args.file}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red][-] Error:[/] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
