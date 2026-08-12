import React from 'react';
import { ConceptStatusEvaluation } from '../types';
import { CheckCircle2, AlertTriangle, XCircle, Quote } from 'lucide-react';

interface ConceptBreakdownCardProps {
  evaluations: ConceptStatusEvaluation[];
}

export const ConceptBreakdownCard: React.FC<ConceptBreakdownCardProps> = ({ evaluations }) => {
  return (
    <div className="space-y-3">
      {evaluations.map((item) => {
        let borderClass = 'border-emerald-500/30 bg-emerald-950/10';
        let Icon = CheckCircle2;
        let iconColor = 'text-emerald-400';
        let badgeText = 'Understood (1.0)';
        let badgeStyle = 'badge-strong';

        if (item.status === 'partial') {
          borderClass = 'border-amber-500/30 bg-amber-950/10';
          Icon = AlertTriangle;
          iconColor = 'text-amber-400';
          badgeText = 'Partially Understood (0.5)';
          badgeStyle = 'badge-partial';
        } else if (item.status === 'incorrect') {
          borderClass = 'border-rose-500/30 bg-rose-950/10';
          Icon = XCircle;
          iconColor = 'text-rose-400';
          badgeText = 'Not Understood (0.0)';
          badgeStyle = 'badge-weak';
        }

        return (
          <div
            key={item.concept_id}
            className={`p-4 rounded-xl border ${borderClass} transition-all duration-200`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2.5">
                <Icon className={`w-5 h-5 ${iconColor} shrink-0`} />
                <span className="font-bold text-slate-100 text-sm">
                  {item.concept_id}: {item.concept_id}
                </span>
              </div>
              <span className={badgeStyle}>
                {badgeText}
              </span>
            </div>

            {/* Evidence quote */}
            {item.evidence && (
              <div className="mt-3 pl-3 border-l-2 border-slate-700 py-1 text-xs text-slate-300 flex items-start gap-2 italic">
                <Quote className="w-3.5 h-3.5 text-blue-400 shrink-0 mt-0.5" />
                <span>"{item.evidence}"</span>
              </div>
            )}

            {item.feedback && (
              <p className="mt-2 text-xs text-slate-400">
                {item.feedback}
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
};
