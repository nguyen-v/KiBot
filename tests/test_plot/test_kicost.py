"""
Tests for the KiCost output.

For debug information use:
pytest-3 --log-cli-level debug
"""
import os.path as op
import re
from . import context
import logging
import subprocess

OUT_DIR = 'KiCost'


def convert2csv(ctx, xlsx, skip_empty=False, sheet=None):
    xlsx = ctx.get_out_path(op.join(OUT_DIR, xlsx))
    csv = xlsx[:-4]+'csv'
    logging.debug('Converting to CSV')
    cmd = ['xlsx2csv']
    if skip_empty:
        cmd.append('--skipemptycolumns')
    if sheet:
        cmd.extend(['-n', sheet])
    cmd.append(xlsx)
    cmd.append(csv)
    subprocess.check_output(cmd)
    with open(csv, 'rt') as f:
        content = f.read()
    content = re.sub(r'(\$|Prj) date:,[^,]+', r'\1 date:,', content, 2)
    content = re.sub(r'KiCost[^,]+', 'KiCost', content, 1)
    content = re.sub(r'KiCad Version:,[^,]+', 'KiCad Version:,', content)
    content = re.sub(r'Created:,[^,]+', 'Created:,', content, 1)
    with open(csv, 'wt') as f:
        f.write(content)


def check_simple(ctx, variant):
    if variant:
        variant = '_'+variant
    name = 'simple'+variant+'.xlsx'
    ctx.expect_out_file_d(name)
    convert2csv(ctx, name, skip_empty=True)
    ctx.compare_txt_d2(name[:-4]+'csv')


def test_kicost_simple(test_dir):
    """ External KiCost using variants, very simple case """
    prj = 'kibom-variant_kicost'
    ctx = context.TestContextSCH(test_dir, prj, 'kicost_simple', OUT_DIR)
    ctx.run()
    check_simple(ctx, '')
    check_simple(ctx, 'default')
    check_simple(ctx, 'production')
    check_simple(ctx, 'test')
    ctx.clean_up()


def test_kicost_int_variant(test_dir):
    """ External KiCost using internal variants """
    prj = 'kibom-variant_kicost'
    ctx = context.TestContextSCH(test_dir, prj, 'kicost_int_variant', OUT_DIR)
    ctx.run(extra_debug=True)
    check_simple(ctx, '')
    check_simple(ctx, 'default')
    check_simple(ctx, 'production')
    check_simple(ctx, 'test')
    ctx.clean_up()


def test_kicost_bom_simple(test_dir):
    """ Internal BoM + KiCost, very simple case. With DNF sheet. """
    prj = 'kibom-variant_2c'
    ctx = context.TestContextSCH(test_dir, prj, 'int_bom_kicost_simple_xlsx', OUT_DIR)
    ctx.run(kicost=True)  # , extra_debug=True
    output = prj+'-bom.xlsx'
    ctx.expect_out_file_d(output)
    convert2csv(ctx, output, sheet='Costs')
    csv = output[:-4]+'csv'
    ctx.compare_txt_d2(csv)
    convert2csv(ctx, output, sheet='Costs (DNF)')
    ctx.compare_txt_d2(csv, output[:-5]+'_dnf.csv')
    convert2csv(ctx, output, sheet='Specs')
    ctx.compare_txt_d2(csv, output[:-5]+'_spec.csv')
    convert2csv(ctx, output, sheet='Specs (DNF)')
    ctx.compare_txt_d2(csv, output[:-5]+'_spec_dnf.csv')
    ctx.clean_up()


def test_kicost_bom_sel_dist_1(test_dir):
    """ Internal BoM + KiCost, select distributors (Mouser+Digi-Key). With DNF sheet. """
    prj = 'kibom-variant_2c'
    ctx = context.TestContextSCH(test_dir, prj, 'int_bom_kicost_sel_dist_1_xlsx', OUT_DIR)
    ctx.run(kicost=True, extra_debug=True)  # , extra_debug=True
    output = prj+'-bom.xlsx'
    ctx.expect_out_file_d(output)
    convert2csv(ctx, output, sheet='Costs')
    csv = output[:-4]+'csv'
    ctx.compare_txt_d2(csv, output[:-5]+'_dk_mou.csv')
    convert2csv(ctx, output, sheet='Costs (DNF)')
    ctx.compare_txt_d2(csv, output[:-5]+'_dk_mou_dnf.csv')
    ctx.clean_up()


def test_kicost_bom_merge_1(test_dir):
    """ Internal BoM + KiCost, merging 3 projects. """
    prj = 'merge_1'
    yaml = 'int_bom_kicost_merge_xlsx'
    if context.ki6():
        yaml += '_k6'
    ctx = context.TestContextSCH(test_dir, prj, yaml, OUT_DIR)
    ctx.run(kicost=True)  # , extra_debug=True
    output = prj+'-bom.xlsx'
    ctx.expect_out_file_d(output)
    convert2csv(ctx, output, sheet='Costs')
    csv = output[:-4]+'csv'
    ctx.compare_txt_d2(csv)
