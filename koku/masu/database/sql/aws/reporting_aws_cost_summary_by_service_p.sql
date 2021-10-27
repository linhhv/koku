DELETE FROM {{schema | sqlsafe}}.reporting_aws_cost_summary_by_service_p
WHERE usage_start >= {{start_date}}::date
    AND usage_start <= {{end_date}}::date
    AND source_uuid = {{source_uuid}}
;

INSERT INTO {{schema | sqlsafe}}.reporting_aws_cost_summary_by_service_p (
    id,
    usage_start,
    usage_end,
    usage_account_id,
    account_alias_id,
    organizational_unit_id,
    product_code,
    product_family,
    unblended_cost,
    blended_cost,
    savingsplan_effective_cost,
    markup_cost,
    currency_code,
    source_uuid
)
    SELECT uuid_generate_v4() as id,
        usage_start,
        usage_start as usage_end,
        usage_account_id,
        max(account_alias_id) as account_alias_id,
        max(organizational_unit_id) as organizational_unit_id,
        product_code,
        product_family,
        sum(unblended_cost) as unblended_cost,
        sum(blended_cost) as blended_cost,
        sum(savingsplan_effective_cost) as savingsplan_effective_cost,
        sum(markup_cost) as markup_cost,
        max(currency_code) as currency_code,
        {{source_uuid}}::uuid as source_uuid
    FROM {{schema | sqlsafe}}.reporting_awscostentrylineitem_daily_summary
    WHERE usage_start >= {{start_date}}::date
        AND usage_start <= {{end_date}}::date
        AND source_uuid = {{source_uuid}}
    GROUP BY usage_start, usage_account_id, product_code, product_family
;