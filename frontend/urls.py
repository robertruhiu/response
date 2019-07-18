from django.urls import path

from frontend.views import index, UserList
from frontend.views import home,activity,tracker,update_candidateprojects,\
    sample,inprogress,projectinvites,update_finished,invites,\
    projectdetails,pendingproject,terms,dev,pricing,howitworks,privacy,\
    report,credits,onboarddevs,onboardrecruiters,seedevs,seerecruiters,manageprojects,managetransactions,\
    editproject,deleteproject,addproject,edittransactions\
    ,deletetransaction,buildproject,calltoapply,apply,opencalltracker,competitions,newproject,\
    passedquizzes,failedquizzes,pickcandidates,update_finishedopencall,portfolio,experience,closetransaction,\
    editportfolioproject,about,management,grading,storegrades,analytics,ProfileUpdate,Profileget,Talentget,Experienceget,\
    Portfolioget,AllUsers,Userget
from frontend.tasks import reminderforprofiledevs,applyreminder,massmail,submission
from accounts.views import update_profile

app_name = 'frontend'
urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('tracker/<int:id>', tracker, name='tracker'),
    path('dev', dev, name='dev'),
    path('howitworks', howitworks, name='howitworks'),
    path('pricing', pricing, name='pricing'),
    path('report/<int:candidate_id>/<int:transaction_id>', report, name='report'),
    path('privacy', privacy, name='privacy'),
    path('terms', terms, name='terms'),
    path('sample', sample, name='sample'),
    path('credits', credits, name='credits'),
    path('inprogress/', inprogress, name='inprogress'),
    path('invites/', invites, name='invites'),
    path('pendingproject/<int:transaction_id>', pendingproject, name='pendingproject'),
    path('projectdetails/<int:id>', projectdetails, name='projectdetails'),
    path('activity/', activity, name='my-activity'),
    path('update_profile/', update_profile, name='update-profile'),
    path('projectinvites/<int:transaction_id>/', projectinvites, name='update-profile'),
    path('update_finished/<int:candidateproject_id>/<int:transaction_id>', update_finished,
         name='update_finished'),
    path('update_finishedopencall/<int:project_id>/<int:transaction_id>', update_finishedopencall,
         name='update_finishedopencall'),
    path('update_candidateprojects/<int:candidateproject_id>/<int:transaction_id>', update_candidateprojects,
         name='update_candidateprojects'),
    path('onboarddevs',onboarddevs,name='onboarddevs'),
    path('onboardrecruiters',onboardrecruiters,name='onboardrecruiters'),
    path('seedevs',seedevs,name='seedevs'),
    path('seerecruiters',seerecruiters,name='seerecruiters'),
    path('manageprojects',manageprojects,name='manageprojects'),
    path('managetransactions',managetransactions,name='managetransactions'),
    path('editproject/<int:project_id>',editproject,name='editproject'),
    path('deleteproject/<int:project_id>',deleteproject,name='deleteproject'),
    path('edittransactions/<int:transaction_id>',edittransactions,name='edittransactions'),
    path('deletetransaction/<int:transaction_id>',deletetransaction,name='deletetransaction'),
    path('closetransaction/<int:transaction_id>',closetransaction,name='closetransaction'),
    path('addproject',addproject,name='addproject'),
    path('calltoapply',calltoapply,name='calltoapply'),
    path('buildproject',buildproject,name='buildproject'),
    path('passedquizzes',passedquizzes,name='passedquizzes'),
    path('failedquizzes',failedquizzes,name='failedquizzes'),
    path('competitions',competitions,name='competitions'),
    path('apply/<int:opportunity_id>',apply,name='apply'),
    path('opencalltracker/<int:trans_id>',opencalltracker,name='opencalltracker'),
    path('pickcandidates/<int:trans_id>/<int:candidate_id>',pickcandidates,name='pickcandidates'),
    path('reminderforprofiledevs',reminderforprofiledevs,name='reminderforprofiledevs'),
    path('applyreminder', applyreminder, name='applyreminder'),
    path('massmail', massmail, name='massmail'),
    path('submission', submission, name='submission'),
    path('portfolio',portfolio,name='portfolio'),
    path('analytics',analytics,name='analytics'),

    path('newproject',newproject,name='newproject'),
    path('experience',experience,name='experience'),
    path('editportfolioproject/<int:project_id>',editportfolioproject,name='editportfolioproject'),
    path('about',about,name='about'),
    path('management',management,name='management'),
    path('grading/<int:candidate_id>/<int:transaction_id>',grading,name='grading'),
    path('storegrades/<int:candidate_id>/<int:transaction_id>',storegrades,name='storegrades'),
    path('users/', UserList.as_view()),
    path('allusers/', AllUsers.as_view()),
    path('updater/<int:pk>', ProfileUpdate.as_view()),
    path('getuser/<int:pk>', Userget.as_view()),
    path('getprofile/<int:pk>', Profileget.as_view()),
    path('gettalent/<int:pk>', Talentget.as_view()),
    path('getexperience/<int:candidate_id>', Experienceget.as_view()),
    path('getportofolio/<int:candidate_id>', Portfolioget.as_view()),



]
