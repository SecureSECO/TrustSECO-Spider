const pynode = require('@fridgerator/pynode');
pynode.startInterpreter();

pynode.appendSysPath('src/env/Lib/site-packages');
pynode.appendSysPath('src');

pynode.openFile('interface');

function testFunc(imput, callback){
    pynode.call('testfunc', imput, callback)
}

///region GitHub
function gh_get_contributor_count(owner, repo, callback){
    pynode.call('gh_get_contributor_count',owner, repo, callback)
}

function gh_get_repository_user_count(owner, repo, callback){
    pynode.call('gh_get_repository_user_count', owner, repo, callback)
}

function gh_get_total_download_count(owner, repo, callback){
    pynode.call('gh_get_total_download_count',owner,repo,callback)
}

function gh_get_release_download_count(owner, repo, release, callback){
    pynode.call('gh_get_release_download_count', owner, repo, release, callback)
}

function gh_get_yearly_commit_count(owner, repo, callback){
    pynode.call('gh_get_yearly_commit_count',owner, repo, callback)
}

function gh_get_commit_count_in_year(owner, repo, year, callback){
    pynode.call('gh_get_commit_count_in_year',owner, repo, year, callback)
}

function gh_get_repository_language(owner, repo, callback){
    pynode.call('gh_get_repository_language',owner, repo, callback)
}

function gh_get_gitstar_ranking(owner, repo, callback){
    pynode.call('gh_get_gitstar_ranking',owner, repo, callback)
}

function gh_get_open_issue_count(owner, repo, callback){
    pynode.call('gh_get_open_issue_count', owner, repo, callback)
}

function gh_get_zero_responses_issue_count(owner, repo, callback){
    pynode.call('gh_get_zero_responses_issue_count', owner, repo, callback)
}

function gh_get_release_issue_count(owner, repo, release, callback){
    pynode.call('gh_get_release_issue_count', owner, repo, release, callback)
}

function gh_get_repository_issue_ratio(owner, repo, callback){
    pynode.call('gh_get_repository_issue_ratio', owner, repo, callback)
}

function gh_get_owner_stargazer_count(owner, callback){
    pynode.call('gh_get_owner_stargazer_count', owner, callback)
}

//libarie io

function lib_get_release_frequency(platform, name, callback){
    pynode.call('lib_get_release_frequency', platform, name, callback)
}

function lib_get_contributor_count(owner, name, callback){
    pynode.call('lib_get_contributor_count', owner, name, callback)
}

function lib_get_dependency_count(platform, name, version, callback){
    pynode.call('lib_get_dependency_count', platform, name, version, callback)
}

function lib_get_dependent_count(platform, name, callback){
    pynode.call('lib_get_dependent_count', platform, name, callback)
}

function lib_get_latest_release_date(platform, name, callback){
    pynode.call('lib_get_latest_release_date', platform, name, callback)
}

function lib_get_first_release_date(platform, name, callback){
    pynode.call('lib_get_first_release_date', platform, name, callback)
}

function lib_get_release_count(platform, name, callback){
    pynode.call('lib_get_release_count', platform, name, callback)
}

function lib_get_sourcerank(platform, name, callback){
    pynode.call('lib_get_sourcerank', platform, name, callback)
}

exports.testFunc = testFunc;
exports.gh_get_contributor_count = gh_get_contributor_count;
exports.gh_get_repository_user_count = gh_get_repository_user_count;
exports.gh_get_total_download_count = gh_get_total_download_count;
exports.gh_get_release_download_count = gh_get_release_download_count;
exports.gh_get_yearly_commit_count = gh_get_yearly_commit_count;
exports.gh_get_commit_count_in_year = gh_get_commit_count_in_year;
exports.gh_get_repository_language = gh_get_repository_language;
exports.gh_get_gitstar_ranking = gh_get_gitstar_ranking;
exports.gh_get_open_issue_count = gh_get_open_issue_count;
exports.gh_get_zero_responses_issue_count = gh_get_zero_responses_issue_count;
exports.gh_get_release_issue_count = gh_get_release_issue_count;
exports.gh_get_repository_issue_ratio = gh_get_repository_issue_ratio;
exports.gh_get_owner_stargazer_count = gh_get_owner_stargazer_count;
exports.lib_get_release_frequency = lib_get_release_frequency;
exports.lib_get_contributor_count = lib_get_contributor_count;
exports.lib_get_dependency_count = lib_get_dependency_count;
exports.lib_get_dependent_count = lib_get_dependent_count;
exports.lib_get_latest_release_date = lib_get_latest_release_date;
exports.lib_get_first_release_date = lib_get_first_release_date;
exports.lib_get_release_count = lib_get_release_count;
exports.lib_get_sourcerank = lib_get_sourcerank;