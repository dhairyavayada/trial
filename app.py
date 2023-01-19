import streamlit as st
import pandas as pd
import math

if __name__ == "__main__":
    # setting header, description and citation
    st.set_page_config(layout="wide")
    
    st.sidebar.markdown('''
    # EH MVP v2.0
    - [Evidence Explorer](#section-1)
    - [Concept Builder](#section-2)
    - [Concept Analyser](#section-3)
    ''', unsafe_allow_html=True)

    st.header('''
    Evidence Explorer
    ''')
    st.write('''
    Enter your search criteria in the fields below then click on Results to explore the published data available that
most closely matches your selections.
The results would display the services and channels used by similar programs along with the expected adoption
rates and outcomes if you were to design your program similarly.
    ''')
    
    uploaded_file = st.file_uploader("Upload References")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        references=0
        references = pd.read_csv(uploaded_file)
    with st.form('Form1'):
        th_area = st.selectbox('Therapy Area', ['Autoimmune/Immunology','Cardiovascular','Endocrine','Gastrointestinal','Infectious disease','Psychiatry','Nephrology','Neurology','Oncology','Pain','Rare Disease','Respiratory','Rheumatology','Vaccines','Ophthalmology','Haematology','Hepatology','Dermatology','Paediatrics','Obstetrics/Gynaecology','Transplant','Other chronic conditions','Other specify'], key=1)         
        cond = st.selectbox('Condition', ['Acromegaly','Ankylosing spondylitis','Asthma','Crohns disease','Diabetes','Erythema nodosum leprosum','Growth hormone deficiency','Hidradenitis suppurativa','High blood pressure','Idiopathic pulmonary fibrosis','Knee osteoarthritis','Major depressive disorder','Multiple myeloma','Multiple sclerosis','Myelodysplastic syndrome','Neovascular age-related macular degeneration','Neuroendocrine tumours','Obesity','Opioid dependence','Osteoporosis','Ostomy surgery','Prostate cancer','Psoriasis','Psoriatic arthritis','Rheumatoid arthritis','Schizophrenia','Ulcerative colitis','Other chronic conditions','Other specify'], key=2)
        drug = st.selectbox('Drug Name', ['Adalimumab','Aflibercept','Aripiprazole','Bisphosphonate ibandronate','Buprenorphine medicationassisted treatment (B-MAT)','Certolizumab','Denosumab','Dimethyl fumarate ','Fingolimod','Glatiramer acetate','Hypoglycaemic agent (OHA)','Infliximab','Insulin','Interferon beta-1a','Interferon beta-1b','Lenalidomide','Liraglutide','Mesalamine','Mitoxantrone','Natalizumab','Nintedanib','Octreotide','Pirfenidone','Pramlintide','Risedronate','Somatropin','Teriparatide','Telmisartan','Teriflunomide','Thalidomide','Vortioxetine','Other specify'], key=4)
        p_stakeholders = st.selectbox('Program Stakeholders', ['GP','Specialist','Patient','Patient-Carer','Nurse','Pharmacist','AHPs','Other clinical staff, specify','Program-management','Partner organisations','Advocacy group','Other specify'], key=5)
        p_strategy = st.selectbox('Program Strategy', ['Supporting quality use of medicines','Providing patient support at-par with industry standard','Providing patient support that exceeds industry standard','Create a new program to be consistent with current enterprise programs','Address an unmet patient need or barrier','Expansion of existing program','Other specify'], key=6)
        roa = st.selectbox('Route of Administration', ['ID','IV','IVI','Oral','Inhale','Topical','SC','Other specify'], key=7)        
        #references = pd.read_csv('dhairyavayada/trial/dataframe3.csv')
        submit_button = st.form_submit_button('View Results')
        references['Sum'] = pd.Series(dtype='int')
        # if ES_15M_Summary.loc[index, 'Rolling_OLS_Coefficient'] > .08:
        for i, row in references.iterrows():
            sum_roa = 0
            sum_drug = 0
            sum_cond = 0
            sum_th = 0
            if str(references.loc[i, 'Route of Administration']) in str(roa):
                sum_roa = 8
            if str(references.loc[i, 'Molecule']) in str(drug):
                sum_drug = 4
            if str(references.loc[i, 'Condition']) in str(cond):
                sum_cond = 2
            if str(references.loc[i, 'Therapy Area']) in th_area:
                sum_th = 1
            references.loc[i, 'Sum'] = sum_roa + sum_drug + sum_cond + sum_th


        sorted_df = references.sort_values(by=['Sum', 'Participants', 'Adoption', 'Program benefit vs non-program'], ascending=False)


        firsts = sorted_df.groupby('Sr', as_index=False).first()


        firsts = firsts.sort_values(by=['Sum', 'Participants'], ascending=False)



        results = firsts.head(10)

        output = results.drop('Sr', axis=1)
        output = output.drop('Sum', axis=1)
                
        results['Participants'] = results['Participants'].astype('int')
        no_participants = results['Participants'].sum()
        #no_programs = results['Condition'].count()
        no_programs = 55

        adoption_rate = results['Adoption'].max()

        program_measure = results['Program Measure']


        prem = results[results['Program Measure'].str.contains('PREM')]
        non_prem = results[~results['Program Measure'].str.contains('PREM')]
        patient_x = prem['Program benefit vs non-program'].max()
        outcome = non_prem['Program benefit vs non-program'].max()

    def remove_dup(x):
        return list(dict.fromkeys(x))
    if submit_button:
        st.write("TRIAL")
        st.write("Based on data from", no_participants, "across ", no_programs, "of programs globally, here are the programs that most closely match your selection \ncriteria.")
        st.write("Best case (from the top 10 programs that most closely match your selection criteria)")
        col1, col2, col3 = st.columns(3)
        col1.metric("Adoption Rate (%)", adoption_rate)
        col2.metric("Patient Experience (%)", patient_x)
        col3.metric("Outcome (%)", outcome)
        display_output = output.pop(output.columns[0])
        st.write("Matches are based on route of administration, condition, therapy area and molecule, in this order.")
        st.write(output)

        
    st.header("Concept Builder")
    
    st.write("Based on selection(s) of program strategy, for your program objective(s) might be recommended below. For strategy around either un-met need or barrier or existing-programs please select any relevant objectives. Also, complete the additional felds below, then press next, to review the potential opportunity for your program concept.")
        

    tag = []
    #print(program_strategy)

    for i in p_strategy:
        if i in ("Supporting quality use of medicines"):
            tag.append("Med")
        elif i in ("Providing patient support at-par with industry standard"):
            tag.append("Low")
        elif i in ("Providing patient support that exceeds industry standard"):
            tag.append("High")
        elif i in ("Create a new program to be consistent with current enterprise programs") or i in ("Expansion of existing program"):
            tag.append("Existing program")
        elif i in ("Address an unmet patient need or barrier"):
            tag.append("Unmet Need")
        else:
            tag.append("Other")
    #print(tag)

    #Step 2: For each program objective, select unique Matched Services (Matrix)

    program_objective = []

    for i in tag:
        if i in "High":
            program_objective.append("Support adherence and persistence")
            program_objective.append("Support complex patient/treatment journey")
            program_objective.append("Best end-to-end experience")
        elif i in "Med":
            program_objective.append("Support end-to-end experience")
            program_objective.append("Support including disease and medicine education")
            program_objective.append("Cross-functional including AHP support")
        elif i in "Low":
            program_objective.append("Disease and medicine education")
        elif i in "Unmet Need":
            program_objective.append("Emotional/psycho-social support")
            program_objective.append("Medication access/financial support")
            program_objective.append("Support carer")
            program_objective.append("HCP support")
        else:
            program_objective.append("Other specify")

    #print(program_objective)
    program_objective = remove_dup(program_objective)

    #progobj = pd.DataFrame(program_objective)
    #progobj.columns = ['Program Objective']

    matched_service = []

    for i in program_objective:
        if i in 'Support adherence and persistence':
            matched_service.append('Patient Education')
            matched_service.append("Side effects/Comorbitity Support")
            matched_service.append("Medicine Usage Support")
            matched_service.append("Medicine Supplies/Logistics")
            matched_service.append("Motivation-Confidence")
        elif i in 'Support complex patient/treatment journey':
            matched_service.append('Patient Education')
            matched_service.append("Side effects/Comorbitity Support")
            matched_service.append("Medicine Usage Support")
            matched_service.append("Medicine Supplies/Logistics")
            matched_service.append("Effective HCP Appointments")
            matched_service.append("Motivation-Confidence")
        elif i in 'Best end-to-end experience':
            matched_service.append('Patient Education')
            matched_service.append("Side effects/Comorbitity Support")
            matched_service.append("Medicine Usage Support")
            matched_service.append("Medicine Supplies/Logistics")
            matched_service.append("Effective HCP Appointments")
            matched_service.append("Motivation-Confidence")
            matched_service.append("Psychosocial-Emotional")
        elif i in 'Support end-to-end experience':
            matched_service.append('Patient Education')
            matched_service.append("Side effects/Comorbitity Support")
            matched_service.append("Medicine Usage Support")
            matched_service.append("Effective HCP Appointments")
            matched_service.append("Motivation-Confidence")
        elif i in 'Support including disease and medicine education':
            matched_service.append('Patient Education')
            matched_service.append("Side effects/Comorbitity Support")
            matched_service.append("Medicine Usage Support")
        elif i in 'Disease and medicine education':
            matched_service.append('Patient Education')
        elif i in 'Emotional/psycho-social support':
            matched_service.append("Motivation-Confidence")
            matched_service.append("Psychosocial-Emotional")
        elif i in 'Medication access/financial support':
            matched_service.append("Financial")
        elif i in 'Support carer':
            matched_service.append('Patient Education')
            matched_service.append("Medicine Usage Support")
            matched_service.append("Carer Enablement")
        elif i in 'Cross-functional including AHP support':
            matched_service.append("Side effects/Comorbitity Support")
            matched_service.append("Effective HCP Appointments")
        elif i in 'HCP support':
            matched_service.append("HCP-Needs")
        else:
            matched_service.append("Other specify")

    matched_service = remove_dup(matched_service)
    #print(matched_service)




    #Step 3: For each matched service, display patient needs 
    pt_needs = []

    for i in matched_service:
        if i in "Patient Education":
            pt_needs.append("Disease education")
            pt_needs.append("Treatment education")
            pt_needs.append("Side effects education")
        elif i in "Carer Enablement":
            pt_needs.append("Carer enablement")
        elif i in "Effective HCP Appointments":
            pt_needs.append("Effective HCP appointments")
            pt_needs.append("Access to HCPs")
            pt_needs.append("Logistics (e.g. transport)")
        elif i in "Financial":
            pt_needs.append("Financial")
        elif i in "Medicine Supplies/Logistics":
            pt_needs.append("Medicine logistics")
            pt_needs.append("ePharmacy")
            pt_needs.append("Convenience")
        elif i in "Medicine Usage Support":
            pt_needs.append("Reminders (medication, appointments, tests)")
            pt_needs.append("Medicine routine")
            pt_needs.append("Monitoring support")
            pt_needs.append("Access to diagnostics/tests/exams")
            pt_needs.append("Supports treatment initiation")
            pt_needs.append("Self-administration")
        elif i in "Motivation-Confidence":
            pt_needs.append("Motivation")
            pt_needs.append("Supports treatment maintenance / persistence")
        elif i in "Psychosocial-Emotional":
            pt_needs.append("Psychosocial")
            pt_needs.append("Peer to peer networking/community")
        elif i in "Sideeffects/Comorbitity Support":
            pt_needs.append("Co-morbidities/co-meds/medication burden")
    pt_needs = remove_dup(pt_needs)
    #print(pt_needs)
    #ptneeds = pd.DataFrame(pt_needs)
    #ptneeds.columns = ['Patient Needs']

    #Step 4: For each matched service, display HCP needs
    #print(matched_service)
    hcp_needs = []
    for i in matched_service:
        if i in "HCP-Needs":
            hcp_needs.append("Administrative burden")
            hcp_needs.append("HCP training")
            hcp_needs.append("Patient support feedback loop")
        elif i in "Medicine Usage Support":
            hcp_needs.append("Complex therapy management")
        elif i in "Patient Education":
            hcp_needs.append("Time poor to deliver patient education/support")
        elif i in "Effective HCP Appointments":
            hcp_needs.append("Multiple stakeholders in patient journey")
        elif i in "Sideeffects/Comorbitity Support":
            hcp_needs.append("Reassurance of care/support outside of their care")
        elif i in "Psychosocial-Emotional":
            hcp_needs.append("Patient support feedback loop")
        elif i in "HCP-Needs":
            hcp_needs.append("HCP training")
        else:
            hcp_needs.append("Other specify")


    hcp_needs = remove_dup(hcp_needs)
    #hcp = pd.DataFrame(hcp_needs)
    #print(hcp_needs)
    #hcp.columns = ['HCP Needs']
    #Step 5: Unique values of sub-services and channels 

    #matched_serv1 = remove_dup(matched_service)
    #matched_serv = pd.DataFrame(matched_serv1)
    #matched_serv.columns = ['Services']
    #print(matched_serv)

    services = remove_dup(results['Services'])
    serv = pd.DataFrame(services)
    serv.columns = ['Services']

    temp = results[results.Services.isin(matched_service)]
    print(temp)

    sub_services = temp['Sub Services']

    #print(sub_services)

    subserv = sub_services.drop_duplicates()
    sub_services = subserv.values.tolist()

    #print(sub_services)

    channels = temp['Channel']
    #print(channels)
    #chnls = pd.DataFrame(channels)
    #chnls.columns = ['Channels']
    chnls = channels.drop_duplicates()
    channels = chnls.values.tolist()

    
    
    with st.form('Form2'):
        probj = st.multiselect(
        'Program Objectives',
        ['Support adherence and persistence','Support complex patient/treatment journey','Best end-to-end experience','Support end-to-end experience','Support including disease and medicine education','Cross-functional including AHP support','Disease and medicine education','Emotional/psycho-social support','Medication access/financial support','Support carer','HCP support','Other specify'],
        program_objective)
        
        prsetting = st.selectbox(
        'Program Setting',
        ('New product launch (PBS)','New product launch (private)','Existing product in market','New indication','Other specify'))
        
        adminfreq = st.selectbox(
        'Administration Frequency',
        ('Daily','Weekly','Fortnightly','Monthly','Quarterly','Twice-yearly','Once-yearly','PRN (as required)','Other specify'))
            
        ptneeds = st.multiselect(
        'Patient Needs',
        ['Disease education','Treatment education','Side effects education','Carer enablement','Effective HCP appointments','Access to HCPs','Logistics (e.g. transport)','Financial','Medicine logistics','ePharmacy','Convenience','Reminders (medication, appointments, tests)','Medicine routine','Monitoring support','Access to diagnostics/tests/exams','Supports treatment initiation','Self-administration','Motivation','Supports treatment maintenance / persistence','Psychosocial','Peer to peer networking/community','Co-morbidities/co-meds/medication burden','Other specify'],
        pt_needs)
        
        hcp = st.multiselect(
        'HCP Needs',
        ['Administrative burden','Complex therapy management','Time poor to deliver patient education/support','Multiple stakeholders in patient journey','Reassurance of care/support outside of their care','Patient support feedback loop','HCP training','Other specify'],
        hcp_needs)       
                
        matched_serv = st.multiselect(
        'Services',
        ['Carer Enablement','Effective HCP Appointments','Financial','HCP-Needs','Medicine Supplies/Logistics','Medicine Usage Support','Motivation-Confidence','Other specify','Patient Education','Psychosocial-Emotional','Side effects/Comobidities Support', 'Side effects/Comorbitity Support'],
        matched_service)
        
        subserv = st.multiselect(
        'Sub-services',
        ['Adherence service','AHPs services','App','Appointment preparation','Approval/Administrative support','Co-pay','Coaching/Counseling','Disposal','Dose support (inc. induction, FDO, titration)','Dose/inj training','Drug administraion/infusion (clinic)','Drug administraion/infusion (home)','e-diary/patient story','Effective HCP Appointments','Email/SMS/Mail','Free-Supply','Goal Setting','HCP/AHP training','Help-line (non-clinical)','Home Delivery/Order','Individual care plan','Insurance support','Logistics-travel','Medicine Usage Support','NA','Nurse/AHP assistance','Partner organisations','Patient care coordination','Patient communities-support','Patient-segmentation','Pharmacy supply','PSP-patient feedback','Psychological intervention','Reminders','Telemonitoring','Testing','Tools-Kits','Vouchers','Website','Welcome Pack', 'Other specify'],
        sub_services)
                                       
        chnls = st.multiselect(
        'Channels',
        ['App','Digital (other)','Email/SMS/Mail','Inperson','NA','Other specify','Partner organisations','Print','Telephone (clinical)','Telephone (non-clinical)','Third-party tool/software','Website','Welcome Pack'],
        channels)
        
        submit_button2 = st.form_submit_button('View Results')
        
        
    def scale(match_services, selection_services, match_channel, selection_channel, outcome):
        if len(selection_services) > len(match_services):
            n = len(selection_services) - len(match_services)
            service_scaling = (1.1)**n
        elif len(selection_services) == len(match_services):
            service_scaling = 1
        else:
            n = len(match_services) - len(selection_services)
            service_scaling = (1.1)/n
        print(service_scaling)
        new_outcome = outcome*service_scaling

        selection_channel_factors = []
        for i in selection_channel:
            if i in "Inperson":
                selection_channel_factors.append(1)
            elif i in "Telephone (clinical)":
                selection_channel_factors.append(0.8)
            elif i in "Welcome Pack":
                selection_channel_factors.append(0.5)
            elif i in "Website":
                selection_channel_factors.append(0.1)
            elif i in "Email/SMS/Mail":
                selection_channel_factors.append(0.2)
            elif i in "Telephone (non-clinical)":
                selection_channel_factors.append(0.5)
            elif i in "App":
                selection_channel_factors.append(0.1)
            elif i in "Partner organisations":
                selection_channel_factors.append(0.2)
            elif i in "Third-party tool/software":
                selection_channel_factors.append(0.2)
            elif i in "Other (specify)":
                selection_channel_factors.append(0.4)
            else:
                selection_channel_factors.append(1)

        match_channel_factors = []
        for i in match_channel:
            if i in "Inperson":
                match_channel_factors.append(1)
            elif i in "Telephone (clinical)":
                match_channel_factors.append(0.8)
            elif i in "Welcome Pack":
                match_channel_factors.append(0.5)
            elif i in "Website":
                match_channel_factors.append(0.1)
            elif i in "Email/SMS/Mail":
                match_channel_factors.append(0.2)
            elif i in "Telephone (non-clinical)":
                match_channel_factors.append(0.5)
            elif i in "App":
                match_channel_factors.append(0.1)
            elif i in "Partner organisations":
                match_channel_factors.append(0.2)
            elif i in "Third-party tool/software":
                match_channel_factors.append(0.2)
            elif i in "Other (specify)":
                match_channel_factors.append(0.4)
            else:
                match_channel_factors.append(1)
        print(selection_channel_factors)
        print(match_channel_factors)
        channel_scaling = max(selection_channel_factors)/max(match_channel_factors)
        print()
        print(channel_scaling)

        new_outcome = new_outcome*channel_scaling

        if new_outcome >= 2*outcome:
            new_outcome = 2*outcome
        elif new_outcome <= 0.5*outcome:
            new_outcome = 0.5*outcome
        print(new_outcome)
        return new_outcome

    outcome = output['Program benefit vs non-program'].max()
    closest_outcome = outcome/100


    display_outcome = scale(matched_service, matched_serv, channels, chnls, closest_outcome)
    display_outcome = math.trunc((display_outcome*100))

    if submit_button2:

        st.metric(label="Opportunity Calculator (% improvement in outcome)", value=display_outcome)
    
    st.header("Concept Analyser")
    
    st.write('Welcome to the Concept analyser.')
    st.write('To forecast the projected 5-year financials and to help predict concept sustainability, please complete the additional fields below to the best of your knowledge.')
    
    with st.form('Form3'):
        
        st.write('**Program Adoption Goals**')
        ca_1 = st.number_input('Patients on drug, (Year 1)')
        ca_2 = st.number_input('New patients on drug, (Year 2)')
        ca_3 = st.number_input('Patients on program, (Year 1)')
        ca_4 = st.number_input('New patients on program, (Year 2)')
        annual_growth = st.number_input('Annual Growth')
        proactive_support_window = st.selectbox(
            "Proactive Support Window",
            ('Welcome only','Initial year only','Ongoing'))
        
        st.write('**Program Compliance Benefits**')
        ca_5 = st.number_input('Standard units per pt per year')
        ca_6 = st.number_input('Additional units per pt per yr')
        
        st.write('**Program Content**')
        promotional_tactics = st.multiselect(
        'Promotional Tactice',
        ['Print mailer','EDMs','Advertising','Field force','Conferences','Demo devices','Packaging insert','Prescribing software','Pharmacy software','Partner organisations'])
        
        matched_serv2 = st.multiselect(
        'Services',
        ['Carer Enablement','Effective HCP Appointments','Financial','HCP-Needs','Medicine Supplies/Logistics','Medicine Usage Support','Motivation-Confidence','Other specify','Patient Education','Psychosocial-Emotional','Side effects/Comobidities Support', 'Side effects/Comorbitity Support'],
        matched_service)
        
        chnls2 = st.multiselect(
        'Channels',
        ['App','Digital (other)','Email/SMS/Mail','Inperson','NA','Other specify','Partner organisations','Print','Telephone (clinical)','Telephone (non-clinical)','Third-party tool/software','Website','Welcome Pack'],
        channels)  
        
        st.write('**Financial**')
        ca_7 = st.number_input('Unit Price (AUD)')
        ca_8 = st.number_input('Budget ($)')
        
        st.write('**Program costs (edit the default values as appropriate based on known or expected amounts for these program components)**')
        
        st.write("Setup (year 1) - Fixed")
        c1, c2, c3 = st.columns(3)
        a1 = c1.number_input("Scoping/SOP/Engagement", value=30000)
        b1 = c2.number_input("Creative/content/materials", value=50000)
        c1 = c3.number_input("Program management", value=20000)
        
        st.write("Ongoing (year 2+) - Fixed")
        c4, c5, c6 = st.columns(3)
        a2 = c4.number_input("Scoping/SOP/Engagement ", value=6000)
        b2 = c5.number_input("Creative/content/materials ", value=10000)
        c2 = c6.number_input("Program management ", value=20000)
    
        st.write('**Services costs (edit the default values as appropriate based on known or expected amounts for these services)**')
        st.write('Setup (year 1) - fixed')
        c7, c8, c9, c10, c11, c12, c13, c14 = st.columns(8)
        a3 = c7.number_input("Program Management", value=20000)
        b3 = c8.number_input("In-person", value=60000)
        c3 = c9.number_input("Telephone (Clin.)", value=30000)
        d3 = c10.number_input("Telephone (non-clin.)", value=0)
        e3 = c11.number_input("Email/SMS/Mail", value=5000)
        f3 = c12.number_input("Website", value=30000)
        g3 = c13.number_input("App", value=100000)
        h3 = c14.number_input("Other", value=5000)
        
        st.write('Ongoing (year 2+) - fixed')
        c15, c16, c17, c18, c19, c20, c21, c22 = st.columns(8)
        a4 = c15.number_input("Program Management ", value=20000)
        b4 = c16.number_input("In-person ", value=20000)
        c4 = c17.number_input("Telephone (Clin.) ", value=10000)
        d4 = c18.number_input("Telephone (non-clin.) ", value=0)
        e4 = c19.number_input("Email/SMS/Mail ", value=5000)
        f4 = c20.number_input("Website ", value=15000)
        g4 = c21.number_input("App ", value=10000)
        h4 = c22.number_input("Other ", value=5000)
        
        st.write('Annual fee per patient - variable')
        c23, c24, c25, c26, c27, c28, c29, c30 = st.columns(8)
        a5 = c23.number_input("Program Management  ", value=50)
        b5 = c24.number_input("In-person  ", value=600)
        c5 = c25.number_input("Telephone (Clin.)  ", value=200)
        d5 = c26.number_input("Telephone (non-clin.)  ", value=0)
        e5 = c27.number_input("Email/SMS/Mail  ", value=50)
        f5 = c28.number_input("Website  ", value=0)
        g5 = c29.number_input("App  ", value=0)
        h5 = c30.number_input("Other  ", value=0)       
        
        st.write('Annual cost - variable')
        c30, c31, c32, c33, c34, c35, c36, c37 = st.columns(8)
        a6 = c30.number_input("Program Management   ", value=5000)
        b6 = c31.number_input("In-person   ", value=60000)
        c6 = c32.number_input("Telephone (Clin.)   ", value=20000)
        d6 = c33.number_input("Telephone (non-clin.)   ", value=0)
        e6 = c34.number_input("Email/SMS/Mail   ", value=5000)
        f6 = c35.number_input("Website   ", value=0)
        g6 = c36.number_input("App   ", value=0)
        h6 = c37.number_input("Other   ", value=0)
        
        
        program_costs = a1 + b1 +c1 + a2 + b2 + c2
        services_cost_setup = a3 + b3 + c3 + d3 + e3 + f3 + g3 + h3
        annual_var_services_cost = a6 + b6 + c6 + d6 + e6 + f6 + g6 + h6
        
        total_cost = program_costs + services_cost_setup + annual_var_services_cost

        #Calculations
        if (ca_3 == 0):
            ca_3 = 1
        if ca_4 == 0:
            ca_4 = 1
        adoption_1 = ca_1/(ca_3)
        adoption_2 = ca_2/(ca_4)
        
        if ca_6 == 0:
            ca_6 = 1
        adoption_3 = ca_5/(ca_6)
        
        def ca(adoption_rate, annual_growth, additional_units):

            no_pts_new_1 = round(ca_3,1)
            no_pts_new_2 = ca_2
            no_pts_new_3 = (1+annual_growth)*ca_2
            no_pts_new_4 = (1+annual_growth)*no_pts_new_3
            no_pts_new_5 = (1+annual_growth)*no_pts_new_4
            no_pts_new_total = no_pts_new_1 + no_pts_new_2 + no_pts_new_3 + no_pts_new_4 + no_pts_new_5

            no_pts_ongoing_1 = round(ca_3,1)
            if proactive_support_window in ('Ongoing'):
                no_pts_ongoing_2 = ca_4 + no_pts_ongoing_1*0.8
                no_pts_ongoing_3 = ca_4 + no_pts_ongoing_2*0.8
                no_pts_ongoing_4 = no_pts_ongoing_3*1.8
                no_pts_ongoing_5 = round(no_pts_ongoing_4*1.8,1)
            else:
                no_pts_ongoing_2 = no_pts_ongoing_1
                no_pts_ongoing_3 = no_pts_ongoing_2
                no_pts_ongoing_4 = no_pts_ongoing_3
                no_pts_ongoing_5 = round(no_pts_ongoing_4,1)

            no_pts_ongoing_total = no_pts_ongoing_1 + no_pts_ongoing_2 + no_pts_ongoing_3 + no_pts_ongoing_4 + no_pts_ongoing_5

            fixed_setup_costs_1 = round(100000,1)
            fixed_setup_costs_2 = 36000
            for i in chnls2:
                if i in ('Inperson'):
                    fixed_setup_costs_1 += 60000
                    fixed_setup_costs_2 += 20000
                elif i in ('Program management'):
                    fixed_setup_costs_1 += 20000
                    fixed_setup_costs_2 += 20000
                elif i in ('Telephone (clinical)'):
                    fixed_setup_costs_1 += 30000
                    fixed_setup_costs_2 += 10000
                elif i in ('Website'):
                    fixed_setup_costs_1 += 30000
                    fixed_setup_costs_2 += 15000
                elif i in ('Email/SMS/Mail'):
                    fixed_setup_costs_1 += 5000
                    fixed_setup_costs_2 += 5000
                elif i in ('Telephone (non-clinical)'):
                    fixed_setup_costs_1 += 10000
                    fixed_setup_costs_2 += 5000
                elif i in ('App'):
                    fixed_setup_costs_1 += 100000
                    fixed_setup_costs_2 += 100000
                elif i in ('Partner organisations'):
                    fixed_setup_costs_1 += 5000
                    fixed_setup_costs_2 += 2500
                elif i in ('Third-party tool/software'):
                    fixed_setup_costs_1 += 5000
                    fixed_setup_costs_2 += 2500


            fixed_setup_costs_3 = fixed_setup_costs_2
            fixed_setup_costs_4 = fixed_setup_costs_2
            fixed_setup_costs_5 = fixed_setup_costs_2
            fixed_setup_costs_total = fixed_setup_costs_2


        #Change logic - look at services cost table
            var_costs_1 = 1
            var_costs_2 = 1
            var_costs_3 = 1
            var_costs_4 = 1
            var_costs_5 = 1
            chnls_list = chnls2
            chnls_list = [item for sublist in chnls_list for item in sublist]

            print(chnls_list)
            for i in chnls_list:
                if i in ('Program management'):
                    var_costs_1 += 50*no_pts_ongoing_1
                    var_costs_2 += 50*no_pts_ongoing_2
                    var_costs_3 += 50*no_pts_ongoing_3
                    var_costs_4 += 50*no_pts_ongoing_4
                    var_costs_5 += 50*no_pts_ongoing_5
                elif i in ('Inperson'):
                    var_costs_1 += 600*no_pts_ongoing_1
                    print(var_costs_1)
                    var_costs_2 += 600*no_pts_ongoing_2
                    var_costs_3 += 600*no_pts_ongoing_3
                    var_costs_4 += 600*no_pts_ongoing_4
                    var_costs_5 += 600*no_pts_ongoing_5
                elif i in ('Telephone (clinical)'):
                    var_costs_1 += 200*no_pts_ongoing_1
                    var_costs_2 += 200*no_pts_ongoing_2
                    var_costs_3 += 200*no_pts_ongoing_3
                    var_costs_4 += 200*no_pts_ongoing_4
                    var_costs_5 += 200*no_pts_ongoing_5
                elif i in ('Welcome Pack'):
                    var_costs_1 += 150*no_pts_ongoing_1
                    var_costs_2 += 150*no_pts_ongoing_2
                    var_costs_3 += 150*no_pts_ongoing_3
                    var_costs_4 += 150*no_pts_ongoing_4
                    var_costs_5 += 150*no_pts_ongoing_5
                elif i in ('Email/SMS/Mail'):
                    var_costs_1 += 10*no_pts_ongoing_1
                    var_costs_2 += 10*no_pts_ongoing_2
                    var_costs_3 += 10*no_pts_ongoing_3
                    var_costs_4 += 10*no_pts_ongoing_4
                    var_costs_5 += 10*no_pts_ongoing_5
                elif i in ('Telephone (non-clinical)'):
                    var_costs_1 += 100*no_pts_ongoing_1
                    var_costs_2 += 100*no_pts_ongoing_2
                    var_costs_3 += 100*no_pts_ongoing_3
                    var_costs_4 += 100*no_pts_ongoing_4
                    var_costs_5 += 100*no_pts_ongoing_5
                elif i in ('Third-party tool/software'):
                    var_costs_1 += 100*no_pts_ongoing_1
                    var_costs_2 += 100*no_pts_ongoing_2
                    var_costs_3 += 100*no_pts_ongoing_3
                    var_costs_4 += 100*no_pts_ongoing_4
                    var_costs_5 += 100*no_pts_ongoing_5
            var_costs_1 = round(var_costs_1,2)
            var_costs_5 = round(var_costs_5,2)
            print(var_costs_1)
            var_costs_total = var_costs_1 + var_costs_2 + var_costs_3 + var_costs_4 + var_costs_5

            total_costs_1 = round(fixed_setup_costs_1 + var_costs_1,1)
            total_costs_2 = fixed_setup_costs_2 + var_costs_2
            total_costs_3 = fixed_setup_costs_3 + var_costs_3
            total_costs_4 = fixed_setup_costs_4 + var_costs_4
            total_costs_5 = round(fixed_setup_costs_5 + var_costs_5,2)
            total_costs_total = total_costs_1 + total_costs_2 + total_costs_3 + total_costs_4 + total_costs_5

            rev_1 = no_pts_ongoing_1*ca_7*ca_6
            rev_2 = no_pts_ongoing_2*ca_7*ca_6
            rev_3 = no_pts_ongoing_3*ca_7*ca_6
            rev_4 = no_pts_ongoing_4*ca_7*ca_6
            rev_5 = no_pts_ongoing_5*ca_7*ca_6
            rev_total = rev_1 + rev_2 + rev_3 + rev_4 + rev_5

            net_1 = round(rev_1 - total_costs_1,1)
            net_2 = rev_2 - total_costs_2
            net_3 = rev_3 - total_costs_3
            net_4 = rev_4 - total_costs_4
            net_5 = round(rev_5 - total_costs_5,2)
            net_total = net_1 + net_2 + net_3 + net_4 + net_5

            cumulative_1 = round(net_1,1)
            cumulative_2 = cumulative_1 + net_2
            cumulative_3 = cumulative_2 + net_3
            cumulative_4 = cumulative_3 + net_4
            cumulative_5 = cumulative_4 + net_5
            cumulative_total = cumulative_1 + cumulative_2 + cumulative_3 + cumulative_4 + cumulative_5 

            d = {'Items': ['No. pts new', 'No. pts ongoing', 'Fixed setup costs', 'Variable costs', 'Total costs', 'Revenue - improved compliance', 'Net income/loss', 'Cumulative income/loss'], 
            'Year 1': [no_pts_new_1, no_pts_ongoing_1, fixed_setup_costs_1, var_costs_1, total_costs_1, rev_1, net_1, cumulative_1],
            'Year 2': [no_pts_new_2, no_pts_ongoing_2, fixed_setup_costs_2, var_costs_2, total_costs_2, rev_2, net_2, cumulative_2],
            'Year 3': [no_pts_new_3, no_pts_ongoing_3, fixed_setup_costs_3, var_costs_3, total_costs_3, rev_3, net_3, cumulative_3],
            'Year 4': [no_pts_new_4, no_pts_ongoing_4, fixed_setup_costs_4, var_costs_4, total_costs_4, rev_4, net_4, cumulative_4],
            'Year 5': [no_pts_new_5, no_pts_ongoing_5, fixed_setup_costs_5, var_costs_5, total_costs_5, rev_5, net_5, cumulative_5],
            'Total': [no_pts_new_total, no_pts_ongoing_total, fixed_setup_costs_total, var_costs_total, total_costs_total, rev_total, net_total, cumulative_total]}

            ca_output = pd.DataFrame(data=d)

            return ca_output

        ca_output = ca(adoption_1, annual_growth, ca_6)
        submit_button3 = st.form_submit_button('Go')

    #Calculations
    if submit_button3:
        col1, col2, col3 = st.columns(3)
        col1.metric("Adoption Rate (Year 1) (%)", math.trunc((adoption_1)*100))
        col2.metric("Adoption Rate (Year 2) (%)", math.trunc((adoption_2)*100))
        col3.metric("Compliance Improvement", math.trunc((adoption_3)*100))
                    
        st.metric(label="Total Estimated Cost", value=total_cost, delta=ca_8,
        delta_color="off", help='Estimated cost compared to budget')
        
        st.write('Based on the selected design settings, with a program adoption rate of', math.trunc((adoption_1)*100),'%', 'the projected fnancials to help predict sustainability for this concept are as follows:')
        st.table(ca_output)

        
    st.subheader('ALT1 Scenario')
    with st.form('Form4'):
        c38, c39, c40 = st.columns(3)
        alt1_ar = c38.number_input("ALT1 - Adoption Rate")
        alt1_ygp = c39.number_input("ALT1 - Yearly growth Program")
        alt1_au = c40.number_input("ALT1 - Additional units per pt per yr")
        alt1_output = ca(alt1_ar, alt1_ygp, alt1_au)
        submit_button4 = st.form_submit_button('Go')
    if submit_button4:
        st.table(alt1_output)
