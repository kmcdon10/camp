db = DAL('sqlite://storage.sqlite')

from gluon.tools import *
auth = Auth(db)

#from gluon.contrib.login_methods.rpx_account import RPXAccount
#auth.settings.actions_disabled=['register','change_password','request_reset_password']
#auth.settings.login_form = RPXAccount(request,
#     api_key='569ddf3abd8a0704347caa9e8bb7370a14905b04 ',
#     domain='localhost:8000/blogging_platform3/default/index',
#     url = "http://localhost:8000/blogging_platform3/%s/default/user/login" % request.application)

db.define_table("image",
    Field("title", unique=True),
    Field("file", "upload"),
    format = "%(title)s")

db.define_table('document',
    Field('name'),
    Field('file', 'upload'),
    Field('created_on', 'datetime', default=request.now),
    format='%(name)s')

auth.define_tables(username=False)

db.define_table('page',
    Field('title'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', readable=False, writable=False))

db.define_table('blogpost',
    Field('title'),
    Field('body', 'text'),
    Field('tags', 'list:string'),
    Field('photo_id', 'reference image'),
    Field('document_id', 'reference document', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now),
    Field('blogpage_id', 'reference page', readable=False, writable=False))

db.define_table('comment',
    Field('body', 'text'),
    Field('created_by'),
    Field('created_on', 'datetime', default=request.now),
    Field('blogpost_id', 'reference blogpost', readable=False, writable=False))


db.document.name.requires = IS_NOT_IN_DB(db, 'document.name')
db.document.created_on.readable = db.document.created_on.writable = False

db.comment.body.requires = IS_NOT_EMPTY()
db.comment.created_by.requires = IS_NOT_EMPTY()
db.comment.created_on.readable = db.comment.created_on.writable = False
db.comment.blogpost_id.requires = IS_IN_DB(db,db.blogpost)

db.blogpost.title.requires = IS_NOT_EMPTY()
db.blogpost.body.requires = IS_NOT_EMPTY()
db.blogpost.blogpage_id.requires = IS_IN_DB(db,db.page)
db.blogpost.photo_id.readable = db.blogpost.photo_id.writable = False
db.blogpost.created_on.readable = db.blogpost.created_on.writable = False

db.page.title.requires = IS_NOT_EMPTY()
db.page.body.reference = IS_NOT_EMPTY()
db.page.created_by.requires = IS_IN_DB(db, db.auth_user)
db.page.created_on.readable = db.page.created_on.writable = False

auth.settings.registration_requires_verification = False

# begin special camps information


db.define_table('staff',
    Field('auth_user_id', 'reference auth_user', default=auth.user_id, update=auth.user_id, readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('first_name', requires=IS_NOT_EMPTY()),
    Field('middle_name', 'text'),
    Field('last_name', requires=IS_NOT_EMPTY()),
    Field('gender', requires=IS_IN_SET(['male', 'female'], zero=T('choose one'), error_message='must choose one')),
    Field('dateofbirth', type='date'),
    Field('street_address', requires=IS_NOT_EMPTY()),
    Field('city', requires=IS_NOT_EMPTY()),
    Field('state', requires=IS_NOT_EMPTY()),
    Field('zipcode', requires=IS_MATCH('^\d{5}(-\d{4})?$', error_message='not a zip code')),
    Field('day_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('evening_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('prefered_name', requires=IS_NOT_EMPTY()),
    Field('shirt_size', requires=IS_IN_SET(['adult_s', 'adult_m', 'adult_l', 'adult_xl', 'adult_2xl', 'adult_3xl'], zero=T('choose one'), error_message='must choose one')),
    Field('email', requires=IS_EMAIL(error_message='invalid email!')),
    Field('drivers_license_or_ssn', requires=IS_NOT_EMPTY()),
    Field('emergency_contact', requires=IS_NOT_EMPTY()),
    Field('emergency_contact_relationship', requires=IS_NOT_EMPTY()),
    Field('emergency_contact_primary_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('emergency_contact_secondary_phone', 'text'),
    Field('convicted_child_related', 'boolean'),
    Field('illegal_drugs', 'boolean'),
    Field('consent_sig_background_check', requires=IS_NOT_EMPTY()),
    Field('consent_sig_date', default=request.now, readable=False, writable=False),
    Field('prefered_position', requires=IS_IN_SET(['nurse', 'activity leader', 'cabin parent'], zero=T('choose one'), error_message='must choose one')),
    Field('can_swim', 'boolean'),
    Field('describe_horse_exp', requires=IS_NOT_EMPTY()),
    Field('special_training', requires=IS_NOT_EMPTY()),
    Field('prev_experience_special_needs', requires=IS_NOT_EMPTY()),
    Field('has_disability', 'boolean',
        Field('describe_disability', requires=IS_NOT_EMPTY())),
    Field('taking_prescriptions', 'boolean'),
    Field('date_preference', requires=IS_IN_SET(['June 5-10 Teens and Adults', 'June 12-17 Children and Teens'], zero=T('choose one'), error_message='must choose one')),
    Field('willing_to_consider_other_session', 'boolean'),
    Field('part_time_dates', 'text'),
    Field('license_revoked', 'boolean'),
    Field('license_signature', requires=IS_NOT_EMPTY()),
    Field('license_date', default=request.now, readable=False, writable=False),
    Field('first_reference_name', requires=IS_NOT_EMPTY()),
    Field('first_reference_relationship', requires=IS_NOT_EMPTY()),
    Field('first_best_time_call', 'text'),
    Field('first_reference_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('second_reference_name', requires=IS_NOT_EMPTY()),
    Field('second_reference_relationship', requires=IS_NOT_EMPTY()),
    Field('second_best_time_call', 'text'),
    Field('second_reference_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('consent_signature', requires=IS_NOT_EMPTY()),
    Field('waiver_signature', requires=IS_NOT_EMPTY()),
    Field('waiver_date', default=request.now, readable=False, writable=False),
    Field('health_policy_issued_to', requires=IS_NOT_EMPTY()),
    Field('policy_number', requires=IS_NOT_EMPTY()),
    Field('policy_group_number', requires=IS_NOT_EMPTY()))

db.staff.auth_user_id.requires = IS_IN_DB(db, db.auth_user)


db.define_table('counselor',
    Field('auth_user_id', 'reference auth_user', default=auth.user_id, update=auth.user_id, readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('first_name', requires=IS_NOT_EMPTY()),
    Field('middle_name', 'text'),
    Field('last_name', requires=IS_NOT_EMPTY()),
    Field('gender', requires=IS_IN_SET(['male', 'female'], zero=T('choose one'), error_message='must choose one')),
    Field('dateofbirth', type='date'),
    Field('street_address', requires=IS_NOT_EMPTY()),
    Field('city', requires=IS_NOT_EMPTY()),
    Field('state', requires=IS_NOT_EMPTY()),
    Field('zipcode', requires=IS_MATCH('^\d{5}(-\d{4})?$', error_message='not a zip code')),
    Field('phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('shirt_size', requires=IS_IN_SET(['adult_s', 'adult_m', 'adult_l', 'adult_xl', 'adult_2xl', 'adult_3xl'], zero=T('choose one'), error_message='must choose one')),
    Field('nickname', 'text'),
    Field('email',requires=IS_EMAIL(error_message='invalid email!')),
    Field('parents_names', requires=IS_NOT_EMPTY()),
    Field('home_phone', 'text'),
    Field('parents_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('emergency_contact', requires=IS_NOT_EMPTY()),
    Field('emergency_contact_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('health_insurance_company', requires=IS_NOT_EMPTY()),
    Field('policy_number', requires=IS_NOT_EMPTY()),
    Field('convicted_child_related', 'boolean'),
    Field('illegal_drugs', 'boolean'),
    Field('convicted_felony', 'boolean'),
    Field('over_18', 'boolean',
        Field('drivers_license', requires=IS_NOT_EMPTY())),
    Field('consent_sig_background_check', requires=IS_NOT_EMPTY()),
    Field('consent_sig_date', default=request.now, readable=False, writable=False),
    Field('high_school', requires=IS_NOT_EMPTY()),
    Field('grade', requires=IS_NOT_EMPTY()),
    Field('hobbies', requires=IS_NOT_EMPTY()),
    Field('special_training', 'text'),
    Field('can_swim', 'boolean'),
    Field('experience_with_disabilities', requires=IS_NOT_EMPTY()),
    Field('previous_camp_counselor', 'boolean'),
    Field('has_disability', 'boolean',
        Field('describe_disability', requires=IS_NOT_EMPTY())),
    Field('taking_prescriptions', 'boolean'),
    Field('reason_for_volunteering', requires=IS_NOT_EMPTY()),
    Field('date_preference', requires=IS_IN_SET(['June 5-10 Teens and Adults', 'June 12-17 Children and Teens'], zero=T('choose one'), error_message='must choose one')),
    Field('willing_to_consider_other_session', 'boolean'),
    Field('transportation', requires=IS_IN_SET([
        'I\'d like to take the bus to/from White pines. The bus stops at Regal Theatre in Warrenville and Plano High in Plano IL.',
        'I will arrange for my own transportation to and from White Pines Ranch in Oregon, IL'], zero=T('choose one'), error_message='must choose one')),
    Field('first_reference_name', requires=IS_NOT_EMPTY()),
    Field('first_reference_relationship', requires=IS_NOT_EMPTY()),
    Field('first_best_time_call', 'text'),
    Field('first_reference_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('second_reference_name', requires=IS_NOT_EMPTY()),
    Field('second_reference_relationship', requires=IS_NOT_EMPTY()),
    Field('second_best_time_call', 'text'),
    Field('second_reference_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('consent_signature', requires=IS_NOT_EMPTY()),
    Field('waiver_conselor_sig', requires=IS_NOT_EMPTY()),
    Field('waiver_parent_sig', requires=IS_NOT_EMPTY()),
    Field('waiver_date', default=request.now, readable=False, writable=False))

db.counselor.auth_user_id.requires = IS_IN_DB(db, db.auth_user)

db.define_table('camper',
    Field('auth_user_id', 'reference auth_user', default=auth.user_id, update=auth.user_id, readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('first_name', requires=IS_NOT_EMPTY()),
    Field('last_name', requires=IS_NOT_EMPTY()),
    Field('dateofbirth', type='date'),
    Field('gender', requires=IS_IN_SET(['male', 'female'], zero=T('choose one'), error_message='must choose one')),
    Field('street_address', requires=IS_NOT_EMPTY()),
    Field('city', requires=IS_NOT_EMPTY()),
    Field('state', requires=IS_NOT_EMPTY()),
    Field('zipcode', requires=IS_MATCH('^\d{5}(-\d{4})?$', error_message='not a zip code')),
    Field('emergency_contact', requires=IS_NOT_EMPTY()),
    Field('emergency_contact_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('health_insurance_company', requires=IS_NOT_EMPTY()),
    Field('policy_number', requires=IS_NOT_EMPTY()),
    Field('shirt_size', requires=IS_IN_SET(['child_s', 'child_m', 'child_l', 'adult_s', 'adult_m', 'adult_l', 'adult_xl', 'adult_2xl', 'adult_3xl'], zero=T('choose one'), error_message='must choose one')))

db.camper.auth_user_id.requires = IS_IN_DB(db, db.auth_user)

db.define_table('guardian',
    Field('camper_id', 'reference camper', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('primary_full_name', requires=IS_NOT_EMPTY()),
    Field('primary_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('second_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('street_address', requires=IS_NOT_EMPTY()),
    Field('city', requires=IS_NOT_EMPTY()),
    Field('state', requires=IS_NOT_EMPTY()),
    Field('zipcode', requires=IS_MATCH('^\d{5}(-\d{4})?$', error_message='not a zip code')),
    Field('email', requires=IS_EMAIL(error_message='invalid email!')),
    Field('secondary_guardian', 'boolean'),
    Field('secondary_full_name', requires=IS_NOT_EMPTY()),
    Field('secondary_primary_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('secondary_second_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('secondary_email', requires=IS_EMAIL(error_message='invalid email!')),
    Field('secondary_relationship', 'text'),
    Field('relationship', requires=IS_NOT_EMPTY()))

db.guardian.camper_id.requires = IS_IN_DB(db, db.camper)

db.define_table('medical_information',
    Field('camper_id', 'reference camper', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('medical_diagnosis', requires=IS_NOT_EMPTY()),
    Field('metal_age_ability', requires=IS_NOT_EMPTY()),
    Field('seizure_type', requires=IS_NOT_EMPTY()),
    Field('recovery_time', requires=IS_NOT_EMPTY()),
    Field('preexisting_medical_conditions', requires=IS_NOT_EMPTY()),
    Field('psychiatric_disorders', requires=IS_NOT_EMPTY()),
    Field('walks_independently', 'boolean'),
    Field('uses_cane_or_walker', 'boolean'),
    Field('uses_wheelchair', 'boolean'),
    Field('needs_transfer_standby_or_assist', 'boolean'),
    Field('is_independent_toileting', 'boolean'),
    Field('has_bowel_and_bladder_control', 'boolean'),
    Field('wears_depends_or_diaper', 'boolean'),
    Field('describe_needs', 'text'))

db.medical_information.camper_id.requires = IS_IN_DB(db, db.camper)

db.define_table('eating',
    Field('camper_id', 'reference camper', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('food_alergies', 'text'),
    Field('limit_intake_of_certain_foods', 'text'),
    Field('watch_for_overeating', 'boolean'),
    Field('special_diet', 'text'),
    Field('assistance_needed', requires=IS_IN_SET(['no help', 'some help', 'all help', 'serve', 'cut'], zero=T('choose one'), error_message='must choose one')))

db.eating.camper_id.requires = IS_IN_DB(db, db.camper)

db.define_table('behavior',
    Field('camper_id', 'reference camper', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('behavioral_problems', 'boolean'),
    Field('describe_frequency', 'text'),
    Field('describe_management_techniques', 'text'),
    Field('activities_hobbies', 'text'),
    Field('horseback_riding_experience', requires=IS_NOT_EMPTY()))

db.behavior.camper_id.requires = IS_IN_DB(db, db.camper)

db.define_table('transportation',
    Field('camper_id', 'reference camper', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('child_pickup', requires=IS_IN_SET([
        'I\'ll pick up my child Friday at the campground between 12 and 1pm',
        'I\'d like my child to take a coach bus to Regal Cantera Theatre in Warrenville near I88',
        'I\'d like my chld to take a coach bus to Plano High School in Plano IL'],
        zero=T('please choose your preference'),
        error_message='must choose one')))

db.transportation.camper_id.requires = IS_IN_DB(db, db.camper)

db.define_table('new_camper_information',
    Field('camper_id', 'reference camper', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('school_work_name', requires=IS_NOT_EMPTY()),
    Field('town', requires=IS_NOT_EMPTY()),
    Field('teacher_boss', requires=IS_NOT_EMPTY()),
    Field('reference_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('been_away_without_family', 'boolean'),
    Field('homesickness_anticipated', 'boolean'),
    Field('previous_overnight_camp', 'boolean'),
    Field('camp_frequency', 'boolean'),
    Field('where_learn_about_camp', requires=IS_NOT_EMPTY()))

db.new_camper_information.camper_id.requires = IS_IN_DB(db, db.camper)

db.define_table('camp_parent_questionnaire',
    Field('camper_id', 'reference camper', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
    Field('needs_nightlight', 'boolean'),
    Field('needs_bedrails', 'boolean'),
    Field('bathroom_during_night', 'boolean'),
    Field('wanders_at_night', 'boolean'),
    Field('wears_pajamas_helmet_braces_at_bedtime', 'text'),
    Field('can_sleep_on_top_bunk_bed', 'boolean'),
    Field('showering', requires=IS_IN_SET(['total assistance', 'some assistance', 'just supervise', 'no help'], zero=T('choose one'), error_message='must choose one')),
    Field('washing_face_hands', requires=IS_IN_SET(['total assistance', 'some assistance', 'just supervise', 'no help'])),
    Field('brushing_teeth', requires=IS_IN_SET(['total assistance', 'some assistance', 'just supervise', 'no help'], zero=T('choose one'), error_message='must choose one')),
    Field('dressing', requires=IS_IN_SET(['total assistance', 'some assistance', 'just supervise', 'no help'], zero=T('choose one'), error_message='must choose one')),
    Field('undressing', requires=IS_IN_SET(['total assistance', 'some assistance', 'just supervise', 'no help'], zero=T('choose one'), error_message='must choose one')),
    Field('menstrual_care', requires=IS_IN_SET(['total assistance', 'some assistance', 'just supervise', 'no help'], zero=T('choose one'), error_message='must choose one')),
    Field('special_instructions', 'text'),
    Field('regular_bedtime', 'text'),
    Field('regular_wakeup_time', 'text'),
    Field('takes_naps', 'boolean'),
    Field('usual_bedtime_routine', 'text'),
    Field('encouraging_good_behavior', 'text'),
    Field('limiting_poor_behavior', 'text'),
    Field('additional_suggestions', 'text'),
    Field('contact_if_issues', requires=IS_NOT_EMPTY()),
    Field('contact_issues_phone', requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')),
    Field('fears_need_to_know', 'text'),
    Field('friends_paired_with_names_order_by_preference', 'text'),
    Field('other_friends_family', 'text'))

db.camp_parent_questionnaire.camper_id.requires = IS_IN_DB(db, db.camper)
