/*
 * SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
 * SPDX-License-Identifier: LicenseRef-Splunk-8-2021
 *
 */
define([
    "jquery",
    "splunkjs/mvc"], function($, mvc)  {
    class Hook {
        constructor(globalConfig, serviceName, model, util) {
            this.model = model;
            this.util = util;
        }
        onCreate() {
             //No implementation required as of now
        }

        onRender() {
			// Clear passwords on render
			this.model.set("organization_api_key", '');
            $(`[data-name="organization_api_key"]`).find("input").val("");

            if (this.model.get("name") !== undefined && this.model.get("name") !== "") {
                $(`[data-name="url"]`).find("input").attr('disabled', true);
            }
        }
        onSave() {
            //No implementation required as of now
			return true;
        }

		onSaveSuccess() {
            //No implementation required as of now
        }

        onSaveFail() {
            //No implementation required as of now
        }
    }
    return Hook;
});
