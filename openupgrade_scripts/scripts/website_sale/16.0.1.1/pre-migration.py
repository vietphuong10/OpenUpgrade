from openupgradelib import openupgrade


def _fill_add_to_cart_action_value(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE website
        ADD COLUMN IF NOT EXISTS add_to_cart_action VARCHAR
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE website
        SET add_to_cart_action = CASE
            WHEN cart_add_on_page = TRUE THEN 'stay'
            ELSE 'go_to_cart'
        END
        """,
    )


def _convert_ext_view_to_base_view(env):
    sort_view_arch = env.ref("website_sale.sort").arch_db
    grid_view_arch = env.ref("website_sale.add_grid_or_list_option").arch_db
    for sort_view in (
        env["ir.ui.view"]
        .with_context(active_test=False)
        .search(
            [
                ("type", "=", "qweb"),
                ("key", "=", "website_sale.sort"),
            ]
        )
    ):
        sort_view.write(
            {"mode": "primary", "inherit_id": False, "arch_db": sort_view_arch}
        )

    for grid_view in (
        env["ir.ui.view"]
        .with_context(active_test=False)
        .search(
            [
                ("type", "=", "qweb"),
                ("key", "=", "website_sale.add_grid_or_list_option"),
            ]
        )
    ):
        grid_view.write(
            {"mode": "primary", "inherit_id": False, "arch_db": grid_view_arch}
        )


@openupgrade.migrate()
def migrate(env, version):
    _fill_add_to_cart_action_value(env)
    openupgrade.rename_fields(
        env,
        [
            (
                "res.company",
                "res_company",
                "website_sale_onboarding_payment_acquirer_state",
                "website_sale_onboarding_payment_provider_state",
            ),
        ],
    )
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "website_sale_stock_wishlist.ir_cron_send_availability_email",
                "website_sale.ir_cron_send_availability_email",
            ),
        ],
    )
    openupgrade.set_xml_ids_noupdate_value(
        env,
        "website_sale",
        [
            "s_dynamic_snippet_products_000_scss",
            "price_dynamic_filter_template_product_product",
            "dynamic_filter_template_product_product_add_to_cart",
            "dynamic_filter_template_product_product_banner",
            "dynamic_filter_template_product_product_borderless_1",
            "dynamic_filter_template_product_product_borderless_2",
            "dynamic_filter_template_product_product_centered",
            "dynamic_filter_template_product_product_horizontal_card",
            "dynamic_filter_template_product_product_mini_image",
            "dynamic_filter_template_product_product_mini_name",
            "dynamic_filter_template_product_product_mini_price",
            "dynamic_filter_template_product_product_view_detail",
        ],
        False,
    )

    # As of 16, filter_products_price become active=True,
    # so we need to remove old views to regenerate them
    # (they also need to reset to the new arch)
    filter_products_price_views = (
        env["ir.ui.view"]
        .with_context(active_test=False)
        .search(
            [
                ("type", "=", "qweb"),
                ("key", "=", "website_sale.filter_products_price"),
            ]
        )
    )
    if filter_products_price_views:
        filter_products_price_views.unlink()
    _convert_ext_view_to_base_view(env)
