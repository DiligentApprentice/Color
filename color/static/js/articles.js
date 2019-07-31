$(function () {
    $(".publish").click(function () {
        var article_url =  "/articles/create-article/";
        $("#article-form").attr('action', article_url);
        $("#article-form").submit();
    });

    $(".update").click(function () {
        $("input[name='status']").val("P");
        //$("input[name='edited']").prop("checked");
        $("input[name='edited']").val("True");
        $("#article-form").submit();
    });

    $(".draft").click(function () {
        var draft_url = "/articles/create-draft/";
        $("#article-form").attr('action', draft_url);
        $("#article-form").submit();
    });
});
