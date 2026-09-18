"""
Verify all files are in place
"""
import os
import sys

print('=' * 60)
print('FILE VERIFICATION')
print('=' * 60)

def check_file(path, base='..'):
    full_path = os.path.join(base, path)
    exists = os.path.exists(full_path)
    status = '✅' if exists else '❌'
    print(f'{status} {path}')
    return exists

print('\nBackend Files:')
backend_files = [
    'backend/progress_tracking_model.py',
    'backend/evolution_analytics.py',
    'backend/test_evolution_analytics.py',
    'backend/test_evolution_debug.py',
    'backend/test_complete_flow.py',
    'flask_cors_config.py'
]
backend_ok = all(check_file(f) for f in backend_files)

print('\nFrontend Files:')
frontend_files = [
    'src/pages/RoutineBuild.jsx',
    'src/components/charts/SimpleLineChart.jsx',
    'src/components/charts/SimpleBarChart.jsx',
    'src/components/charts/SimplePieChart.jsx',
    'src/services/routineService.js'
]
frontend_ok = all(check_file(f) for f in frontend_files)

print('\nDocumentation:')
doc_files = [
    'EVOLUTION_CHARTS_FINAL_FIX.md',
    'EVOLUTION_QUICK_FIX_GUIDE.md',
    'EVOLUTION_CHARTS_COMPLETE.md',
    'FINAL_SOLUTION_SUMMARY.md',
    'TEST_PROGRESS_TO_EVOLUTION.md'
]
docs_ok = all(check_file(f) for f in doc_files)

print('\n' + '=' * 60)
if backend_ok and frontend_ok and docs_ok:
    print('✅ ALL FILES VERIFIED!')
    print('=' * 60)
    print('\nSystem is ready to use!')
    print('\nNext steps:')
    print('1. Start Flask server: python flask_cors_config.py')
    print('2. Open browser and test the flow')
    print('3. Check FINAL_SOLUTION_SUMMARY.md for instructions')
else:
    print('❌ SOME FILES MISSING')
    print('=' * 60)
    sys.exit(1)
