from collections import OrderedDict
from flask import abort, flash, redirect, render_template, request, url_for

from DataQualityTester import app
from DataQualityTester.lib.exceptions import FileGoneException, \
    InvalidXMLException, ActivityNotFoundException, \
    NoFilteredActivitiesException
from DataQualityTester.models import SuppliedData, Results, TestSet


def package_overview(uuid):
    try:
        response = _package_overview(uuid)
    except (FileGoneException, InvalidXMLException) as e:
        flash(str(e), 'danger')
        return redirect(url_for('home'))
    except NoFilteredActivitiesException:
        if request.args.get('filter') == 'false':
            msg = 'No IATI activities found'
            flash(msg, 'danger')
            return redirect(url_for('home'))
        params = {
            'uuid': uuid,
            'filter': 'false',
        }
        return redirect(url_for('package_overview', **params))
    context = response['data']
    context['params'] = response['params']
    return render_template('overview.html', **context)


def _package_overview(uuid):
    params = {'uuid': str(uuid)}
    params.update(dict(request.args.items()))

    supplied_data = SuppliedData.query.get_or_404(str(uuid))
    filter_activities = params.get('filter') != 'false'
    test_set_id = params.get('test_set')
    test_set = TestSet(test_set_id)

    filter_ = test_set.filter if filter_activities else None

    results = Results(supplied_data, test_set, None, filter_)
    if results.all == []:
        raise NoFilteredActivitiesException
    percentages = results.percentages
    components = OrderedDict()
    for component in test_set.components.values():
        items = [percentages[test] for test in component.tests
                 if test in percentages]
        if len(items) == 0:
            continue
        components[component.name] = sum(items) / len(items)
    context = {
        'results': results,
        'components': components,
        'name': supplied_data.name,
        'test_set': test_set,
    }

    return {
        'success': True,
        'data': context,
        'params': params,
    }


def package_quality_by_component(uuid, component):
    try:
        response = _package_quality_by_component(uuid, component)
    except (FileGoneException, InvalidXMLException) as e:
        flash(str(e), 'danger')
        return redirect(url_for('home'))
    context = response['data']
    context['params'] = response['params']
    return render_template('quality_by_component.html', **context)


def _package_quality_by_component(uuid, component_filter):
    params = {'uuid': str(uuid), 'component': component_filter}
    params.update(dict(request.args.items()))
    supplied_data = SuppliedData.query.get_or_404(str(uuid))
    filter_activities = params.get('filter') != 'false'
    test_set = TestSet(params.get('test_set'))

    component = test_set.components.get(component_filter)
    if not component:
        return abort(404)
    filter_ = test_set.filter if filter_activities else None

    results = Results(supplied_data, test_set, component.tests, filter_)
    context = {
        'results': results,
        'test_set': test_set,
    }

    return {
        'success': True,
        'data': context,
        'params': params,
    }


def package_quality_by_test(uuid, test):
    try:
        response = _package_quality_by_test(uuid, test)
    except (FileGoneException, InvalidXMLException) as e:
        flash(str(e), 'danger')
        return redirect(url_for('home'))
    context = response['data']
    context['params'] = response['params']
    return render_template('quality_by_test.html', **context)


def _package_quality_by_test(uuid, test):
    params = {
        'uuid': str(uuid),
        'test': test,
    }
    params.update(dict(request.args.items()))
    supplied_data = SuppliedData.query.get_or_404(str(uuid))
    filter_activities = params.get('filter') != 'false'
    test_set = TestSet(params.get('test_set'))

    filter_ = test_set.filter if filter_activities else None

    results = Results(supplied_data, test_set, [test], filter_)

    per_page = app.config['PER_PAGE']
    passing_results = results.for_test(params['test'], score=1)
    total_passing = len(passing_results)
    failing_results = results.for_test(params['test'], score=0)
    total_failing = len(failing_results)
    not_relevant_results = results.for_test(params['test'], score=-1)
    total_not_relevant = len(not_relevant_results)
    grouped_results = OrderedDict([
        ('passing', passing_results[:per_page]),
        ('failing', failing_results[:per_page]),
        ('not-relevant', not_relevant_results[:per_page]),
    ])

    # page = int(params.get('page', 1))
    # offset = (page - 1) * per_page
    # pagination = Pagination(
    #     page, app.config['PER_PAGE'], len(failing_results))
    # activities_results = activities_results[offset:offset + per_page]

    context = {
        'grouped_results': grouped_results,
        'total_passing': total_passing,
        'total_failing': total_failing,
        'total_not_relevant': total_not_relevant,
        'test_set': test_set,
    }

    return {
        'success': True,
        'data': context,
        'params': params,
    }


def activity_quality(uuid, iati_identifier):
    try:
        response = _activity_quality(uuid, iati_identifier)
    except ActivityNotFoundException:
        return abort(404)
    context = response['data']
    context['params'] = response['params']
    return render_template('activity.html', **context)


def _activity_quality(uuid, iati_identifier):
    params = {
        'uuid': str(uuid),
        'iati_identifier': iati_identifier,
    }
    supplied_data = SuppliedData.query.get_or_404(str(uuid))
    component_filter = params.get('component')

    test_set_id = app.config['DEFAULT_TEST_SET']
    test_set = TestSet(test_set_id)

    component = test_set.components.get(component_filter)
    tests = component.tests if component else test_set.all_tests

    activity = supplied_data.get_activity(iati_identifier)
    results = activity.test(tests)

    context = {
        'results': results,
        'activity': str(activity),
        'iati_identifier': iati_identifier,
    }

    return {
        'success': True,
        'data': context,
        'params': params,
    }
