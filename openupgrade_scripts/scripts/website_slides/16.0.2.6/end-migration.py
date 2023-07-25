from openupgradelib import openupgrade


def _fill_values_on_slide_slide(env):
    slides = env["slide.slide"].with_context(active_test=False).search([])
    slides._compute_slide_type()
    slides._compute_slides_statistics()


def _fill_nbr_article_on_slide_channel(env):
    env["slide.channel"].with_context(active_test=False).search(
        []
    )._compute_slides_statistics()


@openupgrade.migrate()
def migrate(env, version):
    _fill_values_on_slide_slide(env)
    _fill_nbr_article_on_slide_channel(env)
